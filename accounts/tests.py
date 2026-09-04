from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Classroom, Profile
from challenges.models import Task, Assignment, Submission

User = get_user_model()


class AccountsViewsTests(TestCase):
    """Тестирование функционала аккаунтов, классов и домашних заданий"""

    def setUp(self):
        self.client = Client()
        # Создаем учителя
        self.teacher = User.objects.create_user(username="teacher_ivan", password="password123")
        self.teacher.profile.role = Profile.Role.TEACHER
        self.teacher.profile.save()

        # Создаем ученика
        self.student = User.objects.create_user(username="student_alex", password="password123")
        self.student.profile.role = Profile.Role.STUDENT
        self.student.profile.save()

        # Создаем задачу
        self.task = Task.objects.create(
            title="Калькулятор",
            slug="calculator",
            description="Сделайте калькулятор",
            starter_code="def solution(): pass"
        )

    def test_profile_settings_view(self):
        """Проверка страницы настроек профиля и смены роли"""
        self.client.login(username="student_alex", password="password123")
        response = self.client.get(reverse('profile_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "student_alex")
        self.assertContains(response, "Выйти из аккаунта")

        # Смена роли на учителя
        post_response = self.client.post(reverse('profile_settings'), {
            'change_role': '1',
            'role': Profile.Role.TEACHER
        })
        self.assertEqual(post_response.status_code, 302)
        self.student.profile.refresh_from_db()
        self.assertEqual(self.student.profile.role, Profile.Role.TEACHER)

    def test_classroom_list_teacher_create_class(self):
        """Проверка создания класса учителем"""
        self.client.login(username="teacher_ivan", password="password123")
        response = self.client.get(reverse('classroom_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Создать новый класс")

        post_response = self.client.post(reverse('classroom_list'), {
            'create_class': '1',
            'name': 'Python 10-A'
        })
        self.assertEqual(post_response.status_code, 302)
        new_class = Classroom.objects.filter(teacher=self.teacher, name='Python 10-A').first()
        self.assertIsNotNone(new_class)
        self.assertTrue(len(new_class.code) >= 6)

    def test_classroom_list_student_join_class(self):
        """Проверка вступления ученика в класс по коду"""
        classroom = Classroom.objects.create(
            name="Алгоритмы",
            teacher=self.teacher,
            code="ALG123"
        )

        self.client.login(username="student_alex", password="password123")
        response = self.client.get(reverse('classroom_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Присоединиться к классу")

        post_response = self.client.post(reverse('classroom_list'), {
            'join_class': '1',
            'code': 'ALG123'
        })
        self.assertEqual(post_response.status_code, 302)
        self.assertIn(self.student, classroom.students.all())

    def test_student_assignments_view(self):
        """Проверка отображения назначенных заданий классов для ученика"""
        classroom = Classroom.objects.create(
            name="Математика",
            teacher=self.teacher,
            code="MATH99"
        )
        classroom.students.add(self.student)
        assignment = Assignment.objects.create(classroom=classroom, task=self.task)

        self.client.login(username="student_alex", password="password123")
        response = self.client.get(reverse('student_assignments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Калькулятор")
        self.assertContains(response, "Математика")
        self.assertContains(response, "Нужно решить")

        # После решения статус меняется на "Сдано"
        Submission.objects.create(
            user=self.student,
            task=self.task,
            code="def solution(): return 42",
            status=Submission.Status.PASSED,
            execution_time=0.02
        )
        response_after = self.client.get(reverse('student_assignments'))
        self.assertContains(response_after, "Сдано")
