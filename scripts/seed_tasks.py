# -*- coding: utf-8 -*-
"""
Скрипт генерации и сохранения 300+ задач в базу данных Smart Code.
100 Easy, 100 Medium, 100 Hard с проверенными тест-кейсами.
"""
import os
import sys
import django

# Настройка Django окружения
sys.path.append('d:/Smart_code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import transaction
from challenges.models import Task, Tag, TestCase
from challenges.services.runner import parse_test_inputs
from scripts.easy_tasks import EASY_TASKS
from scripts.medium_tasks import MEDIUM_TASKS
from scripts.hard_tasks import HARD_TASKS

TAG_DEFINITIONS = [
    ('basics', 'Основы', 'secondary'),
    ('math', 'Математика', 'danger'),
    ('strings', 'Строки', 'info'),
    ('arrays', 'Массивы', 'primary'),
    ('dicts', 'Словари и множества', 'success'),
    ('search', 'Поиск и сортировка', 'primary'),
    ('recursion', 'Рекурсия', 'warning'),
    ('dp', 'Динамическое программирование', 'danger'),
    ('oop', 'ООП', 'info'),
]

def seed_all():
    print("=== Начало генерации 300 задач ===")
    
    # 1. Создание тегов
    tag_map = {}
    for slug, name, color in TAG_DEFINITIONS:
        tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name, 'color': color})
        tag_map[slug] = tag
    print(f"Теги подготовлены: {len(tag_map)} тегов.")

    dataset = [
        ('easy', EASY_TASKS[:100]),
        ('medium', MEDIUM_TASKS[:100]),
        ('hard', HARD_TASKS[:100]),
    ]

    total_tasks_created = 0
    total_tests_created = 0

    with transaction.atomic():
        for difficulty, tasks in dataset:
            print(f"\nОбработка задач уровня: {difficulty.upper()} ({len(tasks)} шт.)...")
            
            for t_data in tasks:
                slug = t_data['slug']
                title = t_data['title']
                desc = t_data['desc']
                starter = t_data['starter']
                tags_slugs = t_data.get('tags', ['basics'])
                fn = t_data['fn']
                tests = t_data['tests']

                # Создаем или обновляем задачу
                task, created = Task.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'title': title,
                        'description': desc,
                        'difficulty': difficulty,
                        'starter_code': starter,
                    }
                )
                if created:
                    total_tasks_created += 1

                # Привязываем теги
                assigned_tags = [tag_map[ts] for ts in tags_slugs if ts in tag_map]
                if assigned_tags:
                    task.tags.set(assigned_tags)

                # Удаляем старые тесты для этой задачи
                task.test_cases.all().delete()

                # Создаем тест-кейсы
                num_tests = len(tests)
                for i, args in enumerate(tests, start=1):
                    # Форматируем входные аргументы
                    if len(args) == 1:
                        input_str = repr(args[0])
                    else:
                        input_str = ", ".join(repr(x) for x in args)

                    # Вычисляем ожидаемый результат
                    result = fn(*args)
                    expected_str = repr(result) if not isinstance(result, str) else result

                    # Проверяем, что runner сможет распарсить input_data
                    try:
                        parsed = parse_test_inputs(input_str)
                    except Exception as e:
                        print(f"ВНИМАНИЕ: Ошибка парсинга аргументов в задаче {slug}: {e}")

                    is_hidden = (i == num_tests) and (num_tests > 1)

                    TestCase.objects.create(
                        task=task,
                        input_data=input_str,
                        expected_output=expected_str,
                        is_hidden=is_hidden,
                    )
                    total_tests_created += 1

    print("\n" + "="*50)
    print(f"УСПЕХ! Создано/обновлено задач: {Task.objects.count()}")
    print(f"Всего тест-кейсов в базе данных: {TestCase.objects.count()}")
    for diff in ['easy', 'medium', 'hard']:
        cnt = Task.objects.filter(difficulty=diff).count()
        print(f" - {diff.upper()}: {cnt} задач")
    print("="*50)

if __name__ == '__main__':
    seed_all()

