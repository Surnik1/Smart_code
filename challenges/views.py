import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Submission, Tag
from .forms import TaskForm, TestCaseFormSet
from .services.runner import CodeRunnerService
from .services.ai_service import GeminiAIService


def task_list(request):
    """Список всех доступных задач с сортировкой, фильтрацией по статусу и тегам"""
    sort_by = request.GET.get("sort", "newest")
    status_filter = request.GET.get("status", "all")
    tag_slug = request.GET.get("tag")

    if sort_by == "oldest":
        tasks = Task.objects.all().order_by("created_at")
    elif sort_by == "easy":
        tasks = Task.objects.all().order_by("difficulty", "-created_at")
    elif sort_by == "hard":
        tasks = Task.objects.all().order_by("-difficulty", "-created_at")
    else:
        tasks = Task.objects.all().order_by("-created_at")

    # Предзагрузка тегов для исключения N+1 запросов
    tasks = tasks.prefetch_related("tags", "test_cases")

    # Фильтрация по тегу
    if tag_slug:
        tasks = tasks.filter(tags__slug=tag_slug)

    solved_task_ids = set()
    attempted_task_ids = set()

    if request.user.is_authenticated:
        # Идентификаторы решенных и пытавшихся задач пользователя
        solved_task_ids = set(
            Submission.objects.filter(
                user=request.user, status=Submission.Status.PASSED
            ).values_list("task_id", flat=True)
        )
        all_attempted = set(
            Submission.objects.filter(user=request.user).values_list("task_id", flat=True)
        )
        attempted_task_ids = all_attempted - solved_task_ids

        if status_filter == "solved":
            tasks = tasks.filter(id__in=solved_task_ids)
        elif status_filter == "unsolved":
            tasks = tasks.exclude(id__in=solved_task_ids)

    all_tags = Tag.objects.all()

    return render(
        request,
        "challenges/task_list.html",
        {
            "tasks": tasks,
            "current_sort": sort_by,
            "status_filter": status_filter,
            "current_tag": tag_slug,
            "all_tags": all_tags,
            "solved_task_ids": solved_task_ids,
            "attempted_task_ids": attempted_task_ids,
        },
    )


def task_detail(request, slug):
    """Страница конкретной задачи + интерактивная проверка решения (AJAX & Form)"""
    task = get_object_or_404(Task.objects.prefetch_related("tags", "test_cases"), slug=slug)
    result = None
    current_code = task.starter_code

    if request.method == "POST":
        current_code = request.POST.get("code", "")
        test_cases = task.test_cases.all()

        # Безопасный запуск через CodeRunnerService
        result = CodeRunnerService.execute_solution(current_code, test_cases)

        status_mapping = {
            "passed": Submission.Status.PASSED,
            "failed": Submission.Status.FAILED,
            "timeout": Submission.Status.TIMEOUT,
            "error": Submission.Status.ERROR,
        }
        submission_status = status_mapping.get(result["status"], Submission.Status.ERROR)

        if request.user.is_authenticated:
            Submission.objects.create(
                user=request.user,
                task=task,
                code=current_code,
                status=submission_status,
                execution_time=result.get("execution_time"),
            )

        # Поддержка асинхронных AJAX-запросов от Monaco Editor
        is_ajax = (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            or "application/json" in request.headers.get("Accept", "")
        )
        if is_ajax:
            return JsonResponse({
                "passed": result["passed"],
                "status": result["status"],
                "message": result["message"],
                "execution_time": result.get("execution_time", 0.0),
            })

    return render(
        request,
        "challenges/task_detail.html",
        {"task": task, "result": result, "current_code": current_code},
    )


@login_required
def submission_history(request):
    """История решений пользователя с оптимизацией запросов (select_related)"""
    submissions = (
        Submission.objects.filter(user=request.user)
        .select_related("task")
        .order_by("-created_at")
    )
    return render(
        request, "challenges/submission_history.html", {"submissions": submissions}
    )


@login_required
def create_task(request):
    """Создание задачи с множественными тест-кейсами и тегами"""
    if request.user.profile.role != "teacher":
        messages.error(request, "Только учителя могут создавать задачи!")
        return redirect("task_list")

    if request.method == "POST":
        task_form = TaskForm(request.POST)
        testset = TestCaseFormSet(request.POST)

        if task_form.is_valid() and testset.is_valid():
            task = task_form.save()
            testset.instance = task
            testset.save()

            messages.success(
                request, f"Задача '{task.title}' с тест-кейсами и тегами успешно создана!"
            )
            return redirect("task_list")
    else:
        task_form = TaskForm()
        testset = TestCaseFormSet()

    return render(
        request,
        "challenges/create_task.html",
        {"task_form": task_form, "testset": testset},
    )


@login_required
def api_generate_task(request):
    """API генерации задачи с помощью Gemini для учителей"""
    if request.method != "POST":
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

    if request.user.profile.role != "teacher":
        return JsonResponse({"error": "Доступ запрещен. Только учителя могут генерировать задачи."}, status=403)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
            topic = data.get("topic", "").strip()
        else:
            topic = request.POST.get("topic", "").strip()

        if not topic:
            return JsonResponse({"error": "Пожалуйста, укажите тему для задачи."}, status=400)

        task_data = GeminiAIService.generate_task_draft(topic)
        return JsonResponse({"success": True, "task": task_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def api_code_hint(request, slug):
    """API наводящих подсказок от ИИ-ментора без выдачи готового решения"""
    if request.method != "POST":
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

    task = get_object_or_404(Task, slug=slug)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
            user_code = data.get("code", "").strip()
            last_error = data.get("error", "").strip()
        else:
            user_code = request.POST.get("code", "").strip()
            last_error = request.POST.get("error", "").strip()

        if not user_code:
            return JsonResponse({"error": "Код пуст. Напишите решение, чтобы ИИ мог дать подсказку."}, status=400)

        hint = GeminiAIService.get_code_hint(
            task_title=task.title,
            task_description=task.description,
            user_code=user_code,
            test_error=last_error,
        )
        return JsonResponse({"success": True, "hint": hint})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def api_code_review(request, slug):
    """API анализа сложности, чистоты кода и рефакторинга после решения"""
    if request.method != "POST":
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

    task = get_object_or_404(Task, slug=slug)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
            user_code = data.get("code", "").strip()
        else:
            user_code = request.POST.get("code", "").strip()

        if not user_code:
            return JsonResponse({"error": "Код пуст."}, status=400)

        review = GeminiAIService.review_code(
            task_title=task.title,
            task_description=task.description,
            user_code=user_code,
        )
        return JsonResponse({"success": True, "review": review})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
