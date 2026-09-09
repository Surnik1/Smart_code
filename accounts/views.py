from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomRegistrationForm, ProfileRoleForm, CreateClassForm, JoinClassForm
from .models import Classroom
from challenges.models import Task, Assignment, Submission


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = CustomRegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_settings(request):
    """Настройки профиля: смена роли, статистика и выход из аккаунта"""
    user = request.user
    profile = user.profile
    role_form = ProfileRoleForm(instance=profile)

    # Разрешаем смену роли только если пользователь не имеет привязок к классам
    has_taught_classes = user.taught_classes.exists()
    has_joined_classes = user.joined_classes.exists()
    can_change_role = not has_taught_classes and not has_joined_classes

    if request.method == 'POST' and 'change_role' in request.POST:
        if not can_change_role:
            messages.error(
                request,
                "Невозможно сменить роль: у вас есть привязка к классам. "
                "Покиньте все классы или обратитесь к администратору."
            )
            return redirect('profile_settings')

        role_form = ProfileRoleForm(request.POST, instance=profile)
        if role_form.is_valid():
            role_form.save()
            messages.success(request, f"Ваша роль успешно изменена на '{profile.get_role_display()}'!")
            return redirect('profile_settings')

    # Статистика пользователя
    total_submissions = user.submissions.count()
    solved_count = user.submissions.filter(status=Submission.Status.PASSED).values('task').distinct().count()

    return render(request, 'accounts/settings.html', {
        'profile': profile,
        'role_form': role_form,
        'total_submissions': total_submissions,
        'solved_count': solved_count,
        'can_change_role': can_change_role,
    })


@login_required
def classroom_list(request):
    """Отдельная страница управления классами (создание для учителя, вход по коду для ученика)"""
    user = request.user
    profile = user.profile

    create_class_form = CreateClassForm()
    join_class_form = JoinClassForm()

    if request.method == 'POST':
        if 'create_class' in request.POST and profile.role == 'teacher':
            create_class_form = CreateClassForm(request.POST)
            if create_class_form.is_valid():
                new_class = create_class_form.save(commit=False)
                new_class.teacher = user
                new_class.save()
                messages.success(request, f"Класс '{new_class.name}' успешно создан! Код приглашения: {new_class.code}")
                return redirect('classroom_list')

        elif 'join_class' in request.POST and profile.role == 'student':
            join_class_form = JoinClassForm(request.POST)
            if join_class_form.is_valid():
                code = join_class_form.cleaned_data['code'].strip().upper()
                try:
                    classroom = Classroom.objects.get(code=code)
                    if user in classroom.students.all():
                        messages.warning(request, "Вы уже состоите в этом классе!")
                    else:
                        classroom.students.add(user)
                        messages.success(request, f"Вы успешно присоединились к классу '{classroom.name}'!")
                    return redirect('classroom_list')
                except Classroom.DoesNotExist:
                    messages.error(request, "Класс с таким кодом не найден. Проверьте правильность кода.")

    taught_classes = user.taught_classes.all() if profile.role == 'teacher' else None
    joined_classes = user.joined_classes.all() if profile.role == 'student' else None

    return render(request, 'accounts/classroom_list.html', {
        'profile': profile,
        'create_class_form': create_class_form,
        'join_class_form': join_class_form,
        'taught_classes': taught_classes,
        'joined_classes': joined_classes,
    })


@login_required
def student_assignments(request):
    """Страница заданий из классов (домашние и классные работы)"""
    user = request.user
    profile = user.profile

    if profile.role == 'teacher':
        # Для учителя: все назначенные им задания
        assignments = Assignment.objects.filter(classroom__teacher=user).select_related('classroom', 'task').order_by('-created_at')
    else:
        # Для ученика: задания из классов, в которых он состоит
        assignments = Assignment.objects.filter(classroom__students=user).select_related('classroom', 'task').order_by('-created_at')

    # Идентификаторы задач, успешно решенных данным пользователем
    solved_task_ids = set(
        user.submissions.filter(status=Submission.Status.PASSED).values_list('task_id', flat=True)
    )

    return render(request, 'accounts/assignments.html', {
        'assignments': assignments,
        'solved_task_ids': solved_task_ids,
        'is_teacher': profile.role == 'teacher',
    })


@login_required
def classroom_detail(request, pk):
    """Детальная страница конкретного класса (список учеников + назначение задач)"""
    classroom = get_object_or_404(Classroom, pk=pk)

    # Проверка доступа: только учитель класса или ученик класса
    is_teacher = request.user == classroom.teacher
    is_student = request.user in classroom.students.all()
    if not is_teacher and not is_student and not request.user.is_superuser:
        messages.error(request, "У вас нет доступа к этому классу.")
        return redirect('classroom_list')

    if request.method == 'POST' and 'assign_task' in request.POST:
        if is_teacher:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)

            if not Assignment.objects.filter(classroom=classroom, task=task).exists():
                Assignment.objects.create(classroom=classroom, task=task)
                messages.success(request, f"Задача '{task.title}' успешно назначена классу '{classroom.name}'!")
            else:
                messages.warning(request, "Эта задача уже была назначена данному классу.")
            return redirect('classroom_detail', pk=classroom.pk)
        else:
            messages.error(request, "Только учитель класса может назначать задачи.")
            return redirect('classroom_detail', pk=classroom.pk)

    all_tasks = Task.objects.all() if is_teacher else None
    assigned_tasks = classroom.assignments.select_related('task').all()
    students = classroom.students.all()

    return render(request, 'accounts/classroom_detail.html', {
        'classroom': classroom,
        'students': students,
        'all_tasks': all_tasks,
        'assigned_tasks': assigned_tasks,
        'is_teacher': is_teacher,
    })