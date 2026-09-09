from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from challenges.models import Task, TestCase as TaskTestCase, Submission, Tag
from challenges.services.runner import CodeRunnerService, parse_test_inputs, SecurityError

User = get_user_model()


class SecuritySandboxTests(TestCase):
    """Тестирование песочницы и блокировки вредоносного кода"""

    def setUp(self):
        self.task = Task.objects.create(
            title="Тестовая задача",
            slug="test-task",
            description="Сложите два числа",
            starter_code="def solution(a, b):\n    return a + b",
        )
        TaskTestCase.objects.create(
            task=self.task,
            input_data="2, 3",
            expected_output="5",
        )

    def test_block_direct_import(self):
        """Проверка блокировки обычного импорта (import os)"""
        malicious_code = """
def solution(a, b):
    import os
    return 5
"""
        result = CodeRunnerService.execute_solution(malicious_code, self.task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'error')
        self.assertIn("Импорт модулей запрещен", result['message'])

    def test_block_from_import(self):
        """Проверка блокировки импорта через from ... import"""
        malicious_code = """
def solution(a, b):
    from sys import exit
    return 5
"""
        result = CodeRunnerService.execute_solution(malicious_code, self.task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'error')
        self.assertIn("Импорт модулей через 'from ... import' запрещен", result['message'])

    def test_block_dunder_traversal(self):
        """Проверка блокировки побега из песочницы через dunder-атрибуты (__class__, __subclasses__)"""
        malicious_code = """
def solution(a, b):
    subclasses = ().__class__.__bases__[0].__subclasses__()
    return 5
"""
        result = CodeRunnerService.execute_solution(malicious_code, self.task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'error')
        self.assertIn("Доступ к приватным и специальным атрибутам", result['message'])

    def test_block_dangerous_calls(self):
        """Проверка запрета вызова опасных встроенных функций (open, eval, exec)"""
        for func_name in ['open', 'eval', 'exec', 'compile']:
            code = f"""
def solution(a, b):
    {func_name}('some_arg')
    return 5
"""
            result = CodeRunnerService.execute_solution(code, self.task.test_cases.all())
            self.assertFalse(result['passed'])
            self.assertEqual(result['status'], 'error')
            self.assertIn(f"Вызов функции '{func_name}' запрещен", result['message'])

    def test_safe_input_parsing(self):
        """Проверка безопасного парсинга тест-кейсов без выполнения eval"""
        # Корректные аргументы
        self.assertEqual(parse_test_inputs("1, 2"), [1, 2])
        self.assertEqual(parse_test_inputs("[1, 2, 3]"), [[1, 2, 3]])
        self.assertEqual(parse_test_inputs("'hello', 'world'"), ['hello', 'world'])
        self.assertEqual(parse_test_inputs(""), [])


class CodeRunnerExecutionTests(TestCase):
    """Тестирование корректности прогона решений и тестов"""

    def setUp(self):
        self.task = Task.objects.create(
            title="Сумма чисел",
            slug="sum-numbers",
            description="Функция должна возвращать сумму a и b",
            starter_code="def solution(a, b):\n    pass",
        )
        TaskTestCase.objects.create(
            task=self.task,
            input_data="10, 20",
            expected_output="30",
            is_hidden=False,
        )
        TaskTestCase.objects.create(
            task=self.task,
            input_data="-5, 5",
            expected_output="0",
            is_hidden=True,
        )

    def test_successful_solution(self):
        """Проверка правильного решения: все тесты пройдены"""
        correct_code = """
def solution(a, b):
    return a + b
"""
        result = CodeRunnerService.execute_solution(correct_code, self.task.test_cases.all())
        self.assertTrue(result['passed'])
        self.assertEqual(result['status'], 'passed')
        self.assertIn("Все тесты (2 шт.) успешно пройдены", result['message'])
        self.assertGreaterEqual(result['execution_time'], 0.0)

    def test_failed_test_case(self):
        """Проверка ошибочного решения: тест не пройден"""
        wrong_code = """
def solution(a, b):
    return a * b
"""
        result = CodeRunnerService.execute_solution(wrong_code, self.task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'failed')
        self.assertIn("Тест #1 не пройден", result['message'])

    def test_syntax_error(self):
        """Проверка обработки синтаксической ошибки в коде пользователя"""
        broken_code = "def solution(a, b):\n return a +"
        result = CodeRunnerService.execute_solution(broken_code, self.task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'error')
        self.assertIn("Синтаксическая ошибка", result['message'])

    def test_missing_solution_function(self):
        """Проверка отсутствия целевой функции solution"""
        no_func_code = "a = 5\nb = 10"
        result = CodeRunnerService.execute_solution(no_func_code, self.task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'error')
        self.assertIn("Функция 'solution' не найдена", result['message'])

    def test_zero_test_cases(self):
        """Проверка задачи, у которой нет ни одного тест-кейса"""
        empty_task = Task.objects.create(
            title="Пустая задача",
            slug="empty-task",
            description="Нет тестов",
        )
        result = CodeRunnerService.execute_solution("def solution(): pass", empty_task.test_cases.all())
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'error')
        self.assertIn("еще не настроены проверочные тест-кейсы", result['message'])

    def test_timeout_protection(self):
        """Проверка прерывания бесконечного цикла по таймауту"""
        infinite_loop_code = """
def solution(a, b):
    while True:
        pass
"""
        result = CodeRunnerService.execute_solution(infinite_loop_code, self.task.test_cases.all(), timeout_seconds=1.0)
        self.assertFalse(result['passed'])
        self.assertEqual(result['status'], 'timeout')
        self.assertIn("Превышено время ожидания", result['message'])


class ViewsAndIntegrationTests(TestCase):
    """Тестирование представлений (Views) и интеграции"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="student1", password="password123")
        self.task = Task.objects.create(
            title="Умножение",
            slug="multiply",
            description="Умножьте два числа",
            starter_code="def solution(a, b):\n    pass",
        )
        TaskTestCase.objects.create(
            task=self.task,
            input_data="3, 4",
            expected_output="12",
        )
        GamificationService.seed_achievements()

    def test_task_list_sorting_and_rendering(self):
        """Проверка страницы каталога задач и всех вариантов сортировки"""
        for sort_val in ['newest', 'oldest', 'easy', 'hard']:
            response = self.client.get(reverse('task_list'), {'sort': sort_val})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Каталог задач")
            self.assertContains(response, f'value="{sort_val}" selected')

    def test_task_detail_post_submission(self):
        """Проверка отправки кода на странице задачи авторизованным пользователем"""
        self.client.login(username="student1", password="password123")
        code = "def solution(a, b):\n    return a * b"

        response = self.client.post(
            reverse('task_detail', kwargs={'slug': self.task.slug}),
            {'code': code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Все тесты")

        # Проверка создания Submission в БД
        submission = Submission.objects.filter(user=self.user, task=self.task).first()
        self.assertIsNotNone(submission)
        self.assertEqual(submission.status, Submission.Status.PASSED)
        self.assertIsNotNone(submission.execution_time)

    def test_submission_history_view(self):
        """Проверка страницы истории решений"""
        self.client.login(username="student1", password="password123")
        Submission.objects.create(
            user=self.user,
            task=self.task,
            code="def solution(a, b): return 12",
            status=Submission.Status.PASSED,
            execution_time=0.01,
        )

        response = self.client.get(reverse('submission_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Умножение")
        self.assertContains(response, "Пройдено")

    def test_task_detail_ajax_submission(self):
        """Проверка отправки решения через AJAX (Fetch) и получение JSON ответа"""
        self.client.login(username="student1", password="password123")
        code = "def solution(a, b):\n    return a * b"

        response = self.client.post(
            reverse('task_detail', kwargs={'slug': self.task.slug}),
            {'code': code},
            headers={'x-requested-with': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        data = response.json()
        self.assertTrue(data['passed'])
        self.assertEqual(data['status'], 'passed')
        self.assertIn('Все тесты', data['message'])
        self.assertIn('execution_time', data)

    def test_task_list_status_filtering(self):
        """Проверка фильтрации каталога по статусу (all, solved, unsolved)"""
        self.client.login(username="student1", password="password123")

        # Вторая задача (еще не решенная)
        unsolved_task = Task.objects.create(
            title="Деление",
            slug="divide",
            description="Разделите два числа",
            starter_code="def solution(a, b): pass"
        )

        # Решаем первую задачу
        Submission.objects.create(
            user=self.user,
            task=self.task,
            code="def solution(a, b): return a * b",
            status=Submission.Status.PASSED,
            execution_time=0.01
        )

        # Фильтр "Решенные"
        res_solved = self.client.get(reverse('task_list'), {'status': 'solved'})
        self.assertEqual(res_solved.status_code, 200)
        self.assertContains(res_solved, "Умножение")
        self.assertNotContains(res_solved, "Деление")

        # Фильтр "Не решенные"
        res_unsolved = self.client.get(reverse('task_list'), {'status': 'unsolved'})
        self.assertEqual(res_unsolved.status_code, 200)
        self.assertContains(res_unsolved, "Деление")
        self.assertNotContains(res_unsolved, "Умножение")

    def test_task_list_tag_filtering(self):
        """Проверка фильтрации задач по тегам"""
        tag_math = Tag.objects.create(name="ТестМатематика", slug="test-math", color="danger")
        tag_strings = Tag.objects.create(name="ТестСтроки", slug="test-strings", color="info")

        self.task.tags.add(tag_math)

        task2 = Task.objects.create(
            title="Инвертировать строку",
            slug="reverse-string",
            description="Развернуть строку",
            starter_code="def solution(s): pass"
        )
        task2.tags.add(tag_strings)

        # Фильтр по тегу test-math
        res_math = self.client.get(reverse('task_list'), {'tag': 'test-math'})
        self.assertEqual(res_math.status_code, 200)
        self.assertContains(res_math, "Умножение")
        self.assertNotContains(res_math, "Инвертировать строку")

        # Фильтр по тегу test-strings
        res_str = self.client.get(reverse('task_list'), {'tag': 'test-strings'})
        self.assertEqual(res_str.status_code, 200)
        self.assertContains(res_str, "Инвертировать строку")
        self.assertNotContains(res_str, "Умножение")


from unittest.mock import patch


class GeminiAIIntegrationTests(TestCase):
    """Тестирование AI-эндпоинтов (генерация задач, подсказки, ревью)"""

    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username="student_ai", password="password123")
        self.student.profile.role = 'student'
        self.student.profile.save()

        self.teacher = User.objects.create_user(username="teacher_ai", password="password123")
        self.teacher.profile.role = 'teacher'
        self.teacher.profile.save()

        self.task = Task.objects.create(
            title="Проверка палиндрома",
            slug="palindrome-check",
            description="Проверьте, является ли строка палиндромом.",
            starter_code="def solution(s):\n    pass",
        )
        TaskTestCase.objects.create(
            task=self.task,
            input_data="'racecar'",
            expected_output="True",
        )

    def test_api_generate_task_requires_teacher(self):
        """Проверка: ученик не может вызывать генерацию задач (403)"""
        self.client.login(username="student_ai", password="password123")
        response = self.client.post(
            reverse('api_generate_task'),
            data='{"topic": "Сортировка пузырьком"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Только учителя", response.json()['error'])

    def test_api_generate_task_empty_topic(self):
        """Проверка валидации: пустая тема возвращает 400"""
        self.client.login(username="teacher_ai", password="password123")
        response = self.client.post(
            reverse('api_generate_task'),
            data='{"topic": ""}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("укажите тему", response.json()['error'])

    @patch('challenges.views.GeminiAIService.generate_task_draft')
    def test_api_generate_task_success(self, mock_draft):
        """Успешная генерация задачи учителем через ИИ"""
        mock_draft.return_value = {
            "title": "Фибоначчи",
            "slug": "fibonacci",
            "difficulty": "easy",
            "description": "Верните n-ое число Фибоначчи",
            "starter_code": "def solution(n):\n    pass",
            "suggested_tags": ["Рекурсия"],
            "test_cases": [
                {"input_data": "5", "expected_output": "5", "is_hidden": False}
            ]
        }
        self.client.login(username="teacher_ai", password="password123")
        response = self.client.post(
            reverse('api_generate_task'),
            data='{"topic": "Числа Фибоначчи"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['task']['title'], "Фибоначчи")
        self.assertEqual(data['task']['slug'], "fibonacci")

    def test_api_code_hint_empty_code(self):
        """Запрос подсказки с пустым кодом возвращает 400"""
        self.client.login(username="student_ai", password="password123")
        response = self.client.post(
            reverse('api_code_hint', kwargs={'slug': self.task.slug}),
            data='{"code": ""}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Код пуст", response.json()['error'])

    @patch('challenges.views.GeminiAIService.get_code_hint')
    def test_api_code_hint_success(self, mock_hint):
        """Успешное получение наводящей подсказки"""
        mock_hint.return_value = "Обратите внимание на срез строки [::-1]."
        self.client.login(username="student_ai", password="password123")
        response = self.client.post(
            reverse('api_code_hint', kwargs={'slug': self.task.slug}),
            data='{"code": "def solution(s): return s == s", "error": "Тест не пройден"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['hint'], "Обратите внимание на срез строки [::-1].")

    @patch('challenges.views.GeminiAIService.review_code')
    def test_api_code_review_success(self, mock_review):
        """Успешное проведение code review"""
        mock_review.return_value = "1. Сложность: O(n)\n2. PEP 8: Отлично\n3. Рефакторинг: return s == s[::-1]"
        self.client.login(username="student_ai", password="password123")
        response = self.client.post(
            reverse('api_code_review', kwargs={'slug': self.task.slug}),
            data='{"code": "def solution(s): return s == s[::-1]"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn("Сложность: O(n)", data['review'])

    def test_clean_ai_markdown_sanitizer(self):
        """Проверка очистки формул LaTeX и преобразования в Big-O нотацию"""
        from challenges.services.ai_service import clean_ai_markdown
        raw_text = "Сложность: $\\mathcal{O}(N)$ и $\\mathcal{O}(1)$, переменная $N$."
        cleaned = clean_ai_markdown(raw_text)
        self.assertEqual(cleaned, "Сложность: O(N) и O(1), переменная N.")

    def test_render_markdown_template_filter(self):
        """Проверка преобразования Markdown в HTML тегом render_markdown"""
        from challenges.templatetags.markdown_extras import render_markdown_filter
        raw_md = "**Важные условия:**\n- `solution(s)`\n\n### Заголовок\nСложность $\\mathcal{O}(N)$"
        rendered = render_markdown_filter(raw_md)
        self.assertIn("<strong>Важные условия:</strong>", rendered)
        self.assertIn("<code>solution(s)</code>", rendered)
        self.assertIn("<h3>Заголовок</h3>", rendered)
        self.assertIn("O(N)", rendered)
        self.assertNotIn("\\mathcal", rendered)


from accounts.models import Profile, Classroom, Achievement, UserAchievement
from challenges.models import CodeBattle, Assignment
from challenges.services.runner import execute_custom_test
from challenges.services.gamification_service import GamificationService


class CustomTestRunnerTests(TestCase):
    """Тестирование запуска пользовательских проверок (Custom input) и вывода stdout"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="password123")
        self.task = Task.objects.create(
            title="Сложение",
            slug="addition-test",
            description="Сложите два числа",
            starter_code="def solution(a, b):\n    return a + b",
        )

    def test_execute_custom_test_valid(self):
        code = "def solution(a, b):\n    return a + b"
        result = execute_custom_test(code, "3, 4")
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], '7')

    def test_execute_custom_test_stdout(self):
        code = "def solution(x):\n    print('debug 123')\n    return x * 2"
        result = execute_custom_test(code, "5")
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], '10')
        self.assertIn("debug 123", result['stdout'])

    def test_execute_custom_test_security_error(self):
        code = "def solution(x):\n    import os\n    return x"
        result = execute_custom_test(code, "5")
        self.assertFalse(result['success'])
        self.assertIn("запрещен", result['error'])

    def test_api_custom_test_endpoint(self):
        self.client.login(username="tester", password="password123")
        response = self.client.post(
            reverse('api_custom_test', kwargs={'slug': self.task.slug}),
            data='{"code": "def solution(a, b): return a + b", "custom_input": "10, 20"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['result'], '30')


class GamificationServiceTests(TestCase):
    """Тестирование системы геймификации: начисление XP, стрики, ачивки и лидерборд"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="gamer", password="password123")
        self.task_easy = Task.objects.create(
            title="Легкая задача",
            slug="easy-task",
            difficulty=Task.Difficulty.EASY,
            starter_code="def solution(): return 1",
        )
        # Ачивки теперь создаются через management command, но в тестах сидим вручную
        GamificationService.seed_achievements()

    def test_seed_achievements(self):
        GamificationService.seed_achievements()
        self.assertTrue(Achievement.objects.filter(code='first_blood').exists())
        self.assertTrue(Achievement.objects.filter(code='streak_3').exists())

    def test_on_task_passed_xp_and_streak(self):
        # Create a submission for the user
        submission = Submission.objects.create(
            task=self.task_easy,
            user=self.user,
            code="def solution(): return 1",
            status=Submission.Status.PASSED,
        )
        result = GamificationService.on_task_passed(self.user, self.task_easy, submission)
        self.assertEqual(result['xp_earned'], 50)
        self.assertEqual(result['streak_days'], 1)
        self.assertTrue(any('Первая кровь' in a for a in result['new_achievements']))
        self.user.profile.refresh_from_db()
        from django.utils import timezone as tz
        current_hour = tz.now().hour
        expected_xp = 100  # task + first_blood
        if 0 <= current_hour < 5:
            expected_xp += 50  # night_owl bonus
        self.assertEqual(self.user.profile.xp, expected_xp)
        self.assertEqual(self.user.profile.level_title, "Junior I")

    def test_repeat_solve_no_double_xp(self):
        # Выдаем ачивку заранее, чтобы она не добавляла XP повторно
        GamificationService.award_achievement(self.user, "first_blood")
        # Если ночное UTC-время — выдаем night_owl тоже, чтобы она не мешала подсчёту
        from django.utils import timezone as tz
        if 0 <= tz.now().hour < 5:
            GamificationService.award_achievement(self.user, "night_owl")
        self.user.profile.refresh_from_db()
        initial_xp = self.user.profile.xp

        sub1 = Submission.objects.create(
            task=self.task_easy,
            user=self.user,
            code="def solution(): return 1",
            status=Submission.Status.PASSED,
        )
        sub2 = Submission.objects.create(
            task=self.task_easy,
            user=self.user,
            code="def solution(): return 1",
            status=Submission.Status.PASSED,
        )
        result = GamificationService.on_task_passed(self.user, self.task_easy, sub2)
        self.assertEqual(result['xp_earned'], 0)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.xp, initial_xp)

    def test_leaderboard_view(self):
        user2 = User.objects.create_user(username="pro_gamer", password="password123")
        self.user.profile.xp = 100
        self.user.profile.save()
        user2.profile.xp = 500
        user2.profile.save()

        self.client.login(username="gamer", password="password123")
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        leaderboard = list(response.context['leaderboard'])
        self.assertEqual(leaderboard[0]['profile'].user.username, "pro_gamer")
        self.assertEqual(leaderboard[1]['profile'].user.username, "gamer")

    def test_level_progression_thresholds(self):
        """Проверка новой шкалы уровней: Middle от 10k, Senior от 100k, Grandmaster от 10M"""
        profile = self.user.profile

        # Junior
        profile.xp = 0
        self.assertEqual(profile.level_number, 1)
        self.assertEqual(profile.level_title, "Junior I")
        self.assertEqual(profile.progress_percent, 0)

        profile.xp = 3000
        self.assertEqual(profile.level_number, 2)
        self.assertEqual(profile.level_title, "Junior II")

        # Middle (от 10 000)
        profile.xp = 10000
        self.assertEqual(profile.level_number, 3)
        self.assertEqual(profile.level_title, "Middle I")
        self.assertEqual(profile.progress_percent, 0)

        profile.xp = 25000  # середина между 10 000 и 40 000
        self.assertEqual(profile.progress_percent, 50)

        profile.xp = 40000
        self.assertEqual(profile.level_number, 4)
        self.assertEqual(profile.level_title, "Middle II")

        # Senior (от 100 000)
        profile.xp = 100000
        self.assertEqual(profile.level_number, 5)
        self.assertEqual(profile.level_title, "Senior I")

        profile.xp = 500000
        self.assertEqual(profile.level_number, 6)
        self.assertEqual(profile.level_title, "Senior II")

        profile.xp = 1500000
        self.assertEqual(profile.level_number, 7)
        self.assertEqual(profile.level_title, "Lead Developer")

        profile.xp = 5000000
        self.assertEqual(profile.level_number, 8)
        self.assertEqual(profile.level_title, "Principal Engineer")

        # Grandmaster (от 10 000 000)
        profile.xp = 9999999
        self.assertEqual(profile.level_number, 8)
        self.assertEqual(profile.level_title, "Principal Engineer")

        profile.xp = 10000000
        self.assertEqual(profile.level_number, 9)
        self.assertEqual(profile.level_title, "Grandmaster")
        self.assertEqual(profile.progress_percent, 100)


class TeacherAnalyticsTests(TestCase):
    """Тестирование панели аналитики учителя и экспорта отчетов в CSV"""

    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username="teacher_test", password="password123")
        self.teacher.profile.role = Profile.Role.TEACHER
        self.teacher.profile.save()

        self.student = User.objects.create_user(username="student_test", password="password123")
        self.student.profile.role = Profile.Role.STUDENT
        self.student.profile.save()

        self.classroom = Classroom.objects.create(name="10-А класс", teacher=self.teacher)
        self.classroom.students.add(self.student)

        self.task = Task.objects.create(
            title="Задание класса",
            slug="class-task",
            starter_code="def solution(): pass",
        )
        self.assignment = Assignment.objects.create(classroom=self.classroom, task=self.task)

    def test_student_forbidden_analytics(self):
        self.client.login(username="student_test", password="password123")
        response = self.client.get(reverse('classroom_analytics', kwargs={'class_id': self.classroom.id}))
        self.assertIn(response.status_code, [302, 403])

    def test_teacher_analytics_view(self):
        self.client.login(username="teacher_test", password="password123")
        response = self.client.get(reverse('classroom_analytics', kwargs={'class_id': self.classroom.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10-А класс")
        self.assertContains(response, "student_test")

    def test_export_classroom_csv(self):
        self.client.login(username="teacher_test", password="password123")
        response = self.client.get(reverse('export_classroom_csv', kwargs={'class_id': self.classroom.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        content = response.content.decode('utf-8-sig')
        self.assertIn("Ученик", content)
        self.assertIn("student_test", content)


class InteractiveAIChatTests(TestCase):
    """Тестирование интерактивного диалога с AI-ментором в выдвижном чате"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="chat_user", password="password123")
        self.task = Task.objects.create(
            title="Чат задача",
            slug="chat-task",
            starter_code="def solution(): pass",
        )

    @patch('challenges.views.GeminiAIService.chat_with_mentor')
    def test_api_ai_chat_success(self, mock_mentor):
        mock_mentor.return_value = "Попробуйте использовать цикл while."
        self.client.login(username="chat_user", password="password123")
        response = self.client.post(
            reverse('api_ai_chat', kwargs={'slug': self.task.slug}),
            data='{"message": "Как мне решить эту задачу?", "history": []}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['reply'], "Попробуйте использовать цикл while.")

    def test_api_ai_chat_empty_message(self):
        self.client.login(username="chat_user", password="password123")
        response = self.client.post(
            reverse('api_ai_chat', kwargs={'slug': self.task.slug}),
            data='{"message": ""}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Сообщение не может быть пустым", response.json()['error'])


class CodeBattleTests(TestCase):
    """Тестирование PvP дуэлей 1 на 1 в реальном времени (Code Battle)"""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="player1", password="password123")
        self.user2 = User.objects.create_user(username="player2", password="password123")
        self.task = Task.objects.create(
            title="Битва чисел",
            slug="battle-sum",
            starter_code="def solution(a, b):\n    return a + b",
        )
        TaskTestCase.objects.create(
            task=self.task,
            input_data="5, 7",
            expected_output="12",
        )
        GamificationService.seed_achievements()

    def test_battle_create_and_join(self):
        self.client.login(username="player1", password="password123")
        response = self.client.post(reverse('battle_create'), {'task_id': self.task.id})
        self.assertEqual(response.status_code, 302)
        battle = CodeBattle.objects.filter(creator=self.user1).first()
        self.assertIsNotNone(battle)
        self.assertEqual(battle.status, CodeBattle.Status.WAITING)

        # Player 2 joins
        self.client.login(username="player2", password="password123")
        join_res = self.client.post(reverse('battle_join', kwargs={'battle_id': battle.id}))
        self.assertEqual(join_res.status_code, 302)
        battle.refresh_from_db()
        self.assertEqual(battle.opponent, self.user2)
        self.assertEqual(battle.status, CodeBattle.Status.IN_PROGRESS)

    def test_api_battle_status_and_submit(self):
        battle = CodeBattle.objects.create(
            task=self.task,
            creator=self.user1,
            opponent=self.user2,
            status=CodeBattle.Status.IN_PROGRESS,
        )
        self.client.login(username="player1", password="password123")
        status_res = self.client.get(reverse('api_battle_status', kwargs={'battle_id': battle.id}))
        self.assertEqual(status_res.status_code, 200)
        self.assertEqual(status_res.json()['status'], 'in_progress')

        # Player 1 submits winning solution
        submit_res = self.client.post(
            reverse('api_battle_submit', kwargs={'battle_id': battle.id}),
            data='{"code": "def solution(a, b): return a + b"}',
            content_type="application/json"
        )
        self.assertEqual(submit_res.status_code, 200)
        battle.refresh_from_db()
        self.assertEqual(battle.status, CodeBattle.Status.FINISHED)
        self.assertEqual(battle.winner, self.user1)
        self.assertTrue(battle.creator_passed)


