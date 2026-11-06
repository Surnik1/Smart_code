# -*- coding: utf-8 -*-
"""
Mock Users & Activity Seeder for SmartCode.
Generates 220+ realistic student users, 6 teachers, 6 classrooms,
thousands of submissions, achievements, and 1v1 battle records
so the platform and leaderboard look vibrant, active, and populated.
"""
import os
import sys
import random
from datetime import timedelta
import django

# Setup Django environment
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import Profile, Classroom, Achievement, UserAchievement
from challenges.models import Task, Submission, Assignment, CodeBattle

FIRST_NAMES_MALE = [
    "Алихан", "Санжар", "Диас", "Арман", "Данияр", "Ерасыл", "Чингиз", "Тимур", 
    "Алишер", "Бахытжан", "Даурен", "Мади", "Рустем", "Ислам", "Ильяс", "Нурсултан", 
    "Тамерлан", "Олжас", "Мирас", "Айсултан", "Максим", "Иван", "Артем", "Михаил", 
    "Сослан", "Кирилл", "Илья", "Данил", "Роман", "Александр", "Егор", "Нурбол",
    "Бейбарыс", "Азамат", "Кенесары", "Алдияр", "Касым", "Бексултан", "Жандос", "Адиль"
]

FIRST_NAMES_FEMALE = [
    "Аружан", "Диана", "Амина", "Жания", "Камила", "Мадина", "Анель", "Томирис", 
    "Дана", "Айгерим", "Сабина", "Аделия", "Айзере", "Аяулым", "Карина", "Зарина", 
    "Асель", "Гульназ", "София", "Анна", "Виктория", "Полина", "Алиса", "Ксения", 
    "Дарья", "Мария", "Екатерина", "Инжу", "Мерей", "Аяжан", "Дильназ", "Аида"
]

LAST_NAMES = [
    "Смагулов", "Мухтаров", "Каримов", "Ахметов", "Оспанов", "Сериков", "Болатов", 
    "Нурланов", "Ким", "Ли", "Цой", "Жумабек", "Темирбеков", "Байжанов", "Садвакасов", 
    "Маратов", "Калиев", "Токтаров", "Жусупов", "Ибраев", "Кусаинов", "Амангельдиев", 
    "Морозов", "Новиков", "Козлов", "Васильев", "Смирнов", "Попов", "Касымов", 
    "Сулейменов", "Турсынов", "Сабитов", "Ермеков", "Шарипов", "Исабеков", "Алдабергенов"
]

TEACHER_PROFILES = [
    ("marat_teacher", "Марат", "Оспанов", "Учитель информатики высшей категории"),
    ("elvira_it", "Эльвира", "Каримова", "Преподаватель олимпиадного Python"),
    ("saule_informatics", "Сауле", "Ахметова", "Учитель информатики и алгоритмизации"),
    ("aidos_math", "Айдос", "Смагулов", "Тренер сборной по спортивному кодингу"),
    ("ivan_teacher", "Иван", "Морозов", "Преподаватель структур данных и CS"),
    ("gulnara_daryn", "Гульнара", "Исабекова", "Руководитель проектного кружка Дарын"),
]

CLASSROOM_NAMES = [
    "10-А класс (Информатика & Алгоритмы)",
    "10-Б класс (Основы Python и структуры данных)",
    "11-А класс (Олимпиадное программирование)",
    "11-Б класс (Подготовка к ЕНТ и олимпиадам)",
    "Лицей «Дарын» — Сборная по спортивному кодингу",
    "НИШ ФМН — Кружок алгоритмизации и AI",
]

def translit(text: str) -> str:
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'ә': 'a', 'і': 'i', 'ң': 'n', 'ғ': 'g', 'ү': 'u', 'ұ': 'u', 'қ': 'k',
        'ө': 'o', 'һ': 'h'
    }
    res = []
    for ch in text.lower():
        res.append(mapping.get(ch, ch))
    return "".join(res)

def run():
    print("--- Запуск генерации 220+ реалистичных пользователей и активности ---")
    
    # Загружаем существующие ачивки и задачи
    achievements = {a.code: a for a in Achievement.objects.all()}
    all_tasks = list(Task.objects.all())
    if not all_tasks:
        print("[!] Внимание: задачи не найдены в БД. Сначала выполните python scripts/seed_all.py")
        return

    hashed_password = make_password("student123")
    today = timezone.now().date()
    now = timezone.now()

    # 1. Создание Учителей
    teachers = []
    for uname, fn, ln, bio in TEACHER_PROFILES:
        u, created = User.objects.get_or_create(
            username=uname,
            defaults={
                'first_name': fn,
                'last_name': ln,
                'email': f"{uname}@smartcode.edu.kz",
                'password': hashed_password,
            }
        )
        profile, _ = Profile.objects.get_or_create(user=u)
        profile.role = Profile.Role.TEACHER
        profile.save()
        teachers.append(u)
    print(f"[OK] Создано/проверено {len(teachers)} учителей.")

    # 2. Создание Классов
    classrooms = []
    for i, c_name in enumerate(CLASSROOM_NAMES):
        assigned_teacher = teachers[i % len(teachers)]
        classroom, _ = Classroom.objects.get_or_create(
            name=c_name,
            defaults={
                'teacher': assigned_teacher,
            }
        )
        classrooms.append(classroom)
    print(f"[OK] Создано/проверено {len(classrooms)} классов.")

    # 3. Генерация 220 Учеников
    random.seed(42)  # Стабильный детерминированный посев для воспроизводимости
    created_students = []
    
    # Генерируем уникальные имена
    generated_identities = []
    used_usernames = set(User.objects.values_list('username', flat=True))
    
    while len(generated_identities) < 220:
        is_male = random.random() > 0.48
        first_name = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
        base_last = random.choice(LAST_NAMES)
        if is_male:
            last_name = base_last if base_last in ("Ким", "Ли", "Цой") else (base_last if base_last.endswith(("ов", "ев", "ин")) else base_last + "ов")
        else:
            last_name = base_last if base_last in ("Ким", "Ли", "Цой") else (base_last + "а" if base_last.endswith(("ов", "ев", "ин")) else base_last + "ова")

        fn_t = translit(first_name)
        ln_t = translit(last_name)
        
        patterns = [
            f"{fn_t}_{ln_t[:1]}",
            f"{fn_t}.{ln_t}",
            f"{ln_t}_{fn_t[:1]}",
            f"{fn_t}_code",
            f"{fn_t}_dev",
            f"{fn_t}_algo",
            f"{fn_t}_py",
            f"{fn_t}_{random.randint(10, 99)}",
        ]
        chosen_uname = None
        for p in patterns:
            clean_p = p.replace("'", "").replace(" ", "").replace("-", "_")
            if clean_p not in used_usernames:
                chosen_uname = clean_p
                used_usernames.add(chosen_uname)
                break
        
        if not chosen_uname:
            chosen_uname = f"{fn_t}_{ln_t[:2]}_{random.randint(100, 999)}"
            used_usernames.add(chosen_uname)
            
        generated_identities.append((chosen_uname, first_name, last_name, is_male))

    # Сортируем идентичности по уровням и опыту для красивого лидерборда
    # Топ лидерборда: места 1-5 (Principal / Lead), 6-20 (Senior), 21-60 (Middle), 61-120 (Junior II), 121-220 (Junior I)
    
    print("Создаем пользователей, профили и распределяем по классам...")
    submissions_batch = []
    user_achievements_batch = []
    
    for rank_idx, (uname, fn, ln, is_male) in enumerate(generated_identities, start=1):
        u, created = User.objects.get_or_create(
            username=uname,
            defaults={
                'first_name': fn,
                'last_name': ln,
                'email': f"{uname}@smartcode.edu.kz",
                'password': hashed_password,
            }
        )
        created_students.append(u)
        
        # Распределяем в 1-2 класса
        assigned_classroom = classrooms[rank_idx % len(classrooms)]
        assigned_classroom.students.add(u)
        if random.random() < 0.25:
            extra_classroom = classrooms[(rank_idx + 2) % len(classrooms)]
            extra_classroom.students.add(u)

        # Вычисляем прогресс, XP, Streak по рангу
        if rank_idx <= 5:
            # Топ 5 чемпионов платформы
            xp = random.randint(72000, 98500)
            streak = random.randint(24, 45)
            solved_count = random.randint(48, 72)
            days_ago_solve = 0
        elif rank_idx <= 20:
            # Топ 20 элита
            xp = random.randint(32000, 68000)
            streak = random.randint(14, 28)
            solved_count = random.randint(30, 47)
            days_ago_solve = random.choice([0, 0, 1])
        elif rank_idx <= 60:
            # Продвинутые
            xp = random.randint(12000, 31000)
            streak = random.randint(6, 16)
            solved_count = random.randint(18, 29)
            days_ago_solve = random.choice([0, 1, 1, 2])
        elif rank_idx <= 120:
            # Средний уровень
            xp = random.randint(3500, 11500)
            streak = random.randint(3, 8)
            solved_count = random.randint(8, 17)
            days_ago_solve = random.choice([0, 1, 2, 3])
        elif rank_idx <= 180:
            # Активные новички
            xp = random.randint(1000, 3400)
            streak = random.randint(1, 4)
            solved_count = random.randint(3, 7)
            days_ago_solve = random.randint(1, 5)
        else:
            # Начинающие
            xp = random.randint(150, 950)
            streak = random.randint(0, 2)
            solved_count = random.randint(1, 3)
            days_ago_solve = random.randint(1, 8)

        # Обновляем профиль
        profile, _ = Profile.objects.get_or_create(user=u)
        profile.role = Profile.Role.STUDENT
        profile.xp = xp
        profile.streak_days = streak
        profile.last_solve_date = today - timedelta(days=days_ago_solve) if streak > 0 else None
        profile.save()

        # Генерируем решения задач (Submissions)
        # Выбираем случайные задачи из пула
        solved_tasks = random.sample(all_tasks, min(solved_count, len(all_tasks)))
        
        for task in solved_tasks:
            # Некоторые задачи решались не с первого раза (добавляем 1-2 неудачные попытки)
            if random.random() < 0.4:
                sub_fail_time = now - timedelta(days=random.randint(1, 25), hours=random.randint(1, 20))
                submissions_batch.append(
                    Submission(
                        user=u,
                        task=task,
                        code=task.starter_code or "def solution():\n    pass",
                        status=random.choice([Submission.Status.FAILED, Submission.Status.ERROR]),
                        execution_time=round(random.uniform(0.015, 0.085), 3),
                        created_at=sub_fail_time,
                    )
                )

            # Успешное решение
            sub_pass_time = now - timedelta(days=random.randint(0, days_ago_solve + 15), hours=random.randint(0, 18))
            submissions_batch.append(
                Submission(
                    user=u,
                    task=task,
                    code=task.reference_solution or task.starter_code or "def solution(*args):\n    return True",
                    status=Submission.Status.PASSED,
                    execution_time=round(random.uniform(0.012, 0.095), 3),
                    created_at=sub_pass_time,
                )
            )

        # Присваиваем ачивки по заслугам
        if 'first_blood' in achievements and solved_count >= 1:
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['first_blood']))
        if 'five_tasks' in achievements and solved_count >= 5:
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['five_tasks']))
        if 'ten_tasks' in achievements and solved_count >= 10:
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['ten_tasks']))
        if 'streak_3' in achievements and streak >= 3:
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['streak_3']))
        if 'streak_7' in achievements and streak >= 7:
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['streak_7']))
        if 'night_owl' in achievements and (rank_idx % 4 == 0 or rank_idx <= 10):
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['night_owl']))
        if 'battle_winner' in achievements and rank_idx <= 25:
            user_achievements_batch.append(UserAchievement(user=u, achievement=achievements['battle_winner']))

    # Bulk create Submissions
    print(f"Сохраняем {len(submissions_batch)} решений в базу данных...")
    Submission.objects.filter(user__in=created_students).delete()
    Submission.objects.bulk_create(submissions_batch, batch_size=500)

    # Bulk create UserAchievements (без дубликатов)
    print(f"Сохраняем {len(user_achievements_batch)} ачивок...")
    UserAchievement.objects.filter(user__in=created_students).delete()
    UserAchievement.objects.bulk_create(user_achievements_batch, ignore_conflicts=True, batch_size=500)

    # 4. Создание Заданий для классов (Assignments)
    print("Создаем активные классные задания...")
    for cr in classrooms:
        if cr.assignments.count() < 3:
            assigned_sample = random.sample(all_tasks, 3)
            for t in assigned_sample:
                Assignment.objects.get_or_create(
                    classroom=cr,
                    task=t,
                    defaults={'due_date': now + timedelta(days=random.randint(2, 10))}
                )

    # 5. Создание истории дуэлей 1v1 (Code Battles)
    print("Создаем историю дуэлей Code Battle...")
    CodeBattle.objects.all().delete()
    battles_batch = []
    
    top_students = created_students[:30]
    for b_idx in range(25):
        c1, c2 = random.sample(top_students, 2)
        b_task = random.choice(all_tasks)
        winner = random.choice([c1, c2])
        b_time = now - timedelta(days=random.randint(0, 10), hours=random.randint(1, 12))
        
        battles_batch.append(
            CodeBattle(
                task=b_task,
                creator=c1,
                opponent=c2,
                winner=winner,
                status=CodeBattle.Status.FINISHED,
                creator_code=b_task.reference_solution or "def solution(): pass",
                opponent_code=b_task.reference_solution or "def solution(): pass",
                creator_passed=True,
                opponent_passed=True,
                created_at=b_time,
                started_at=b_time,
                finished_at=b_time + timedelta(minutes=random.randint(2, 7)),
            )
        )

    # 2 активные дуэли в процессе
    active_b1 = random.sample(top_students, 2)
    battles_batch.append(
        CodeBattle(
            task=random.choice(all_tasks),
            creator=active_b1[0],
            opponent=active_b1[1],
            status=CodeBattle.Status.IN_PROGRESS,
            creator_passed=False,
            opponent_passed=False,
            created_at=now - timedelta(minutes=4),
            started_at=now - timedelta(minutes=3),
        )
    )
    active_b2 = random.sample(top_students, 2)
    battles_batch.append(
        CodeBattle(
            task=random.choice(all_tasks),
            creator=active_b2[0],
            opponent=None,
            status=CodeBattle.Status.WAITING,
            creator_passed=False,
            opponent_passed=False,
            created_at=now - timedelta(minutes=1),
        )
    )

    CodeBattle.objects.bulk_create(battles_batch)

    print("\n" + "="*60)
    print("[SUCCESS] Успешно сгенерирована живая активность:")
    print(f"  • Всего пользователей: {User.objects.count()}")
    print(f"  • Из них учеников: {Profile.objects.filter(role=Profile.Role.STUDENT).count()}")
    print(f"  • Из них учителей: {Profile.objects.filter(role=Profile.Role.TEACHER).count()}")
    print(f"  • Классов: {Classroom.objects.count()}")
    print(f"  • Всего отправленных решений (Submissions): {Submission.objects.count()}")
    print(f"  • Выданных ачивок (UserAchievements): {UserAchievement.objects.count()}")
    print(f"  • Дуэлей Code Battle: {CodeBattle.objects.count()}")
    print("="*60)

if __name__ == '__main__':
    run()
