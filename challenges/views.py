import csv
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.db import models
from .models import Task, Submission, Tag, Assignment, CodeBattle
from .models import Task, Submission, Tag, Assignment, CodeBattle, TaskSolutionView
from .forms import TaskForm, TestCaseFormSet
from .services.runner import CodeRunnerService
from .services.ai_service import GeminiAIService
from .services.gamification_service import GamificationService
from accounts.models import Classroom, Profile


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

        gamification_data = None
        if request.user.is_authenticated:
            submission = Submission.objects.create(
                user=request.user,
                task=task,
                code=current_code,
                status=submission_status,
                execution_time=result.get("execution_time"),
            )
            if result.get("passed"):
                gamification_data = GamificationService.on_task_passed(request.user, task, submission)

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
                "stdout": result.get("stdout", ""),
                "gamification": gamification_data,
            })

    has_viewed_solution = False
    if request.user.is_authenticated:
        has_viewed_solution = TaskSolutionView.objects.filter(user=request.user, task=task).exists()

    return render(
        request,
        "challenges/task_detail.html",
        {
            "task": task,
            "result": result,
            "current_code": current_code,
            "has_viewed_solution": has_viewed_solution,
        },
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


@login_required
@require_POST
def api_custom_test(request, slug):
    """AJAX эндпоинт для запуска решения на пользовательских входных данных (отладка/дебаг)"""
    task = get_object_or_404(Task, slug=slug)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    code = data.get("code", "").strip()
    custom_input = data.get("custom_input", "").strip()

    if not code:
        return JsonResponse({"success": False, "error": "Код пуст!"}, status=400)

    result = CodeRunnerService.execute_custom_test(code, custom_input)
    return JsonResponse(result)


@require_POST
def api_ai_chat(request, slug):
    """Интерактивный чат с AI-ментором по конкретной задаче (многошаговый диалог)"""
    task = get_object_or_404(Task, slug=slug)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"success": False, "error": "Неверный формат запроса"}, status=400)

    user_message = data.get("message", "").strip()
    history = data.get("history", [])
    user_code = data.get("code", "").strip()
    test_error = data.get("error", "").strip()

    if not user_message:
        return JsonResponse({"success": False, "error": "Сообщение не может быть пустым"}, status=400)

    try:
        reply = GeminiAIService.chat_with_mentor(
            task_title=task.title,
            task_description=task.description,
            user_code=user_code,
            test_error=test_error,
            user_message=user_message,
            history=history,
        )
        return JsonResponse({"success": True, "reply": reply})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
@require_POST
def api_reveal_solution(request, slug):
    """
    Эндпоинт для ученика, который сдался и запросил эталонный ответ.
    Фиксирует просмотр в TaskSolutionView (блокируя начисление XP и ачивок за задачу)
    и возвращает эталонный код решения и объяснение.
    """
    task = get_object_or_404(Task, slug=slug)

    # Фиксируем отметку о просмотре ответа
    TaskSolutionView.objects.get_or_create(user=request.user, task=task)

    data = GeminiAIService.get_or_generate_solution(task)

    return JsonResponse({
        "success": True,
        "solution": data.get("solution", ""),
        "explanation": data.get("explanation", ""),
        "message": "Эталонное решение открыто. Опыт (XP) и достижения за эту задачу теперь отключены.",
    })


def leaderboard(request):
    """Таблица лидеров (Hall of Fame) платформы и фильтрация по классу"""
    from django.db.models import Count

    class_id = request.GET.get('classroom')
    selected_class = None

    profiles = (
        Profile.objects.filter(role=Profile.Role.STUDENT)
        .select_related('user')
        .prefetch_related('user__achievements__achievement')
    )

    user_classes = []
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.TEACHER:
            user_classes = Classroom.objects.filter(teacher=request.user)
        else:
            user_classes = request.user.joined_classes.all()

    if class_id:
        try:
            selected_class = Classroom.objects.get(id=class_id)
            profiles = profiles.filter(user__in=selected_class.students.all())
        except Classroom.DoesNotExist:
            pass

    leaderboard_list = profiles.order_by('-xp', '-streak_days')[:50]
    user_ids = [p.user_id for p in leaderboard_list]

    solved_counts = {
        item['user']: item['count']
        for item in Submission.objects.filter(user_id__in=user_ids, status=Submission.Status.PASSED)
        .values('user')
        .annotate(count=Count('task', distinct=True))
    }

    leaderboard_data = []
    for rank, prof in enumerate(leaderboard_list, start=1):
        leaderboard_data.append({
            'rank': rank,
            'profile': prof,
            'solved_count': solved_counts.get(prof.user_id, 0),
            'achievements': prof.user.achievements.all()[:4],
        })

    return render(request, 'challenges/leaderboard.html', {
        'leaderboard': leaderboard_data,
        'user_classes': user_classes,
        'selected_class': selected_class,
    })


@login_required
def classroom_analytics(request, class_id):
    """Учительская аналитика: матрица сдачи заданий классом с дедлайнами"""
    classroom = get_object_or_404(Classroom, id=class_id)
    if classroom.teacher != request.user and not request.user.is_superuser:
        messages.error(request, "У вас нет доступа к аналитике этого класса.")
        return redirect('classroom_list')

    assignments = classroom.assignments.select_related('task').order_by('created_at')
    students = classroom.students.select_related('profile').order_by('username')

    student_ids = [s.id for s in students]
    task_ids = [a.task_id for a in assignments]

    submissions = Submission.objects.filter(
        user_id__in=student_ids,
        task_id__in=task_ids,
    ).values('user_id', 'task_id', 'status', 'created_at', 'execution_time')

    matrix = {}
    for s in submissions:
        key = (s['user_id'], s['task_id'])
        if key not in matrix or s['status'] == Submission.Status.PASSED:
            matrix[key] = s

    matrix_rows = []
    for student in students:
        row_tasks = []
        solved_count = 0
        for assign in assignments:
            sub = matrix.get((student.id, assign.task_id))
            status = sub['status'] if sub else 'none'
            if status == Submission.Status.PASSED:
                solved_count += 1

            is_overdue = False
            if assign.due_date and status != Submission.Status.PASSED:
                if timezone.now() > assign.due_date:
                    is_overdue = True

            row_tasks.append({
                'assignment': assign,
                'status': status,
                'is_overdue': is_overdue,
            })

        matrix_rows.append({
            'student': student,
            'tasks': row_tasks,
            'solved_count': solved_count,
            'total_tasks': len(assignments),
            'percent': int((solved_count / len(assignments)) * 100) if assignments else 0,
        })

    return render(request, 'challenges/classroom_analytics.html', {
        'classroom': classroom,
        'assignments': assignments,
        'matrix_rows': matrix_rows,
    })


@login_required
def export_classroom_csv(request, class_id):
    """Экспорт ведомости успеваемости класса в CSV"""
    classroom = get_object_or_404(Classroom, id=class_id)
    if classroom.teacher != request.user and not request.user.is_superuser:
        return HttpResponse("Доступ запрещен", status=403)

    assignments = classroom.assignments.select_related('task').order_by('created_at')
    students = classroom.students.order_by('username')

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="analytics_{classroom.code}.csv"'

    writer = csv.writer(response)
    header = ['Ученик', 'Сдано задач', 'Процент'] + [a.task.title for a in assignments]
    writer.writerow(header)

    student_ids = [s.id for s in students]
    task_ids = [a.task_id for a in assignments]

    submissions = Submission.objects.filter(
        user_id__in=student_ids,
        task_id__in=task_ids,
        status=Submission.Status.PASSED,
    ).values_list('user_id', 'task_id')
    passed_set = set(submissions)

    for student in students:
        solved = 0
        task_statuses = []
        for a in assignments:
            if (student.id, a.task_id) in passed_set:
                task_statuses.append('Сдано')
                solved += 1
            else:
                task_statuses.append('Не сдано')
        pct = f"{int((solved / len(assignments)) * 100)}%" if assignments else "0%"
        writer.writerow([student.username, solved, pct] + task_statuses)

    return response


# --- CODE BATTLE (Дуэли 1 на 1) ---

@login_required
def battle_list(request):
    """Список комнат дуэлей (лобби)"""
    waiting_battles = CodeBattle.objects.filter(status=CodeBattle.Status.WAITING).select_related('task', 'creator')
    active_battles = CodeBattle.objects.filter(
        status=CodeBattle.Status.IN_PROGRESS
    ).filter(
        models.Q(creator=request.user) | models.Q(opponent=request.user)
    ).select_related('task', 'creator', 'opponent')
    all_tasks = Task.objects.all()

    return render(request, 'challenges/battle_lobby.html', {
        'waiting_battles': waiting_battles,
        'active_battles': active_battles,
        'tasks': all_tasks,
    })


@login_required
@require_POST
def battle_create(request):
    """Создание новой дуэльной комнаты"""
    import random
    task_id = request.POST.get('task_id')
    if task_id:
        task = get_object_or_404(Task, id=task_id)
    else:
        # Случайная задача
        tasks = list(Task.objects.all())
        if not tasks:
            messages.error(request, "Нет доступных задач для дуэли.")
            return redirect('battle_list')
        task = random.choice(tasks)

    battle = CodeBattle.objects.create(
        task=task,
        creator=request.user,
        creator_code=task.starter_code,
        opponent_code=task.starter_code,
        status=CodeBattle.Status.WAITING,
    )
    return redirect('battle_arena', battle_id=battle.id)


@login_required
def battle_join(request, battle_id):
    """Присоединение к дуэли соперником"""
    battle = get_object_or_404(CodeBattle, id=battle_id)
    if battle.status != CodeBattle.Status.WAITING:
        messages.warning(request, "Эта дуэль уже началась или завершена.")
        return redirect('battle_list')

    if battle.creator == request.user:
        return redirect('battle_arena', battle_id=battle.id)

    battle.opponent = request.user
    battle.opponent_code = battle.task.starter_code
    battle.status = CodeBattle.Status.IN_PROGRESS
    battle.started_at = timezone.now()
    battle.save()

    return redirect('battle_arena', battle_id=battle.id)


@login_required
def battle_arena(request, battle_id):
    """Арена боя 1 на 1: кодинг с таймером и живым отслеживанием соперника"""
    battle = get_object_or_404(CodeBattle.objects.select_related('task', 'creator', 'opponent', 'winner'), id=battle_id)
    is_creator = (request.user == battle.creator)
    is_opponent = (request.user == battle.opponent)

    if not is_creator and not is_opponent and battle.status != CodeBattle.Status.WAITING:
        messages.error(request, "Вы не являетесь участником этой дуэли.")
        return redirect('battle_list')

    starter_code = battle.creator_code if is_creator else battle.opponent_code
    if not starter_code:
        starter_code = battle.task.starter_code

    return render(request, 'challenges/battle_arena.html', {
        'battle': battle,
        'task': battle.task,
        'is_creator': is_creator,
        'starter_code': starter_code,
    })


@login_required
@require_POST
def api_battle_submit(request, battle_id):
    """Отправка решения в рамках дуэли"""
    battle = get_object_or_404(CodeBattle, id=battle_id)
    is_creator = (request.user == battle.creator)
    is_opponent = (request.user == battle.opponent)

    if not is_creator and not is_opponent:
        return JsonResponse({'success': False, 'error': 'Вы не участник дуэли'}, status=403)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    code = data.get('code', '').strip()
    if is_creator:
        battle.creator_code = code
    else:
        battle.opponent_code = code

    test_cases = battle.task.test_cases.all()
    result = CodeRunnerService.execute_solution(code, test_cases)

    if result['passed']:
        if is_creator:
            battle.creator_passed = True
        else:
            battle.opponent_passed = True

        # Если победитель еще не определен — этот игрок победил!
        if not battle.winner:
            battle.winner = request.user
            battle.status = CodeBattle.Status.FINISHED
            battle.finished_at = timezone.now()
            # Награда гладиатору
            GamificationService.award_achievement(request.user, 'battle_winner')
            prof, _ = Profile.objects.get_or_create(user=request.user)
            prof.add_xp(100)

    battle.save()

    return JsonResponse({
        'success': True,
        'passed': result['passed'],
        'status': result['status'],
        'message': result['message'],
        'battle_status': battle.status,
        'winner': battle.winner.username if battle.winner else None,
        'is_winner': (battle.winner == request.user),
    })


@login_required
def api_battle_status(request, battle_id):
    """Проверка статуса дуэли (опрос соперника)"""
    battle = get_object_or_404(CodeBattle.objects.select_related('winner', 'opponent', 'creator'), id=battle_id)
    return JsonResponse({
        'status': battle.status,
        'has_opponent': battle.opponent is not None,
        'opponent_name': battle.opponent.username if battle.opponent else None,
        'creator_passed': battle.creator_passed,
        'opponent_passed': battle.opponent_passed,
        'winner': battle.winner.username if battle.winner else None,
        'is_winner': (battle.winner == request.user),
    })

