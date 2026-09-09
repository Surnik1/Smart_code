from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """Модель тега/категории задачи (например: Строки, Массивы, Рекурсия)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL-слаг")
    color = models.CharField(max_length=30, default="primary", verbose_name="Стиль/Цвет бейджа")

    def __str__(self):
        return f"#{self.name}"

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']


class Task(models.Model):
    """Модель задачи (Каты)"""
    
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Easy (8-7 kyu)'
        MEDIUM = 'medium', 'Medium (6-4 kyu)'
        HARD = 'hard', 'Hard (3-1 kyu)'

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-слаг")
    description = models.TextField(verbose_name="Описание задачи (Markdown)")
    difficulty = models.CharField(
        max_length=10, 
        choices=Difficulty.choices, 
        default=Difficulty.EASY,
        verbose_name="Сложность"
    )
    starter_code = models.TextField(
        default="def solution():\n    pass", 
        verbose_name="Начальный шаблон кода"
    )
    reference_solution = models.TextField(
        blank=True,
        default="",
        verbose_name="Эталонное решение"
    )
    reference_solution_explanation = models.TextField(
        blank=True,
        default="",
        verbose_name="Пояснение к эталонному решению"
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        related_name='tasks', 
        verbose_name="Теги"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class TestCase(models.Model):
    """Тесты для автоматической проверки решения"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='test_cases', verbose_name="Задача")
    input_data = models.TextField(verbose_name="Входные данные")
    expected_output = models.TextField(verbose_name="Ожидаемый результат")
    is_hidden = models.BooleanField(default=False, verbose_name="Скрытый тест?")

    def __str__(self):
        test_type = "Скрытый" if self.is_hidden else "Открытый"
        return f"{test_type} тест для {self.task.title}"

    class Meta:
        verbose_name = "Тест-кейс"
        verbose_name_plural = "Тест-кейсы"


class Submission(models.Model):
    """Отправленное пользователем решение"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'В очереди'
        PASSED = 'passed', 'Пройдено'
        FAILED = 'failed', 'Ошибка в тестах'
        ERROR = 'error', 'Ошибка выполнения (Runtime Error)'
        TIMEOUT = 'timeout', 'Превышено время ожидания'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', verbose_name="Пользователь")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions', verbose_name="Задача")
    code = models.TextField(verbose_name="Отправленный код")
    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Статус"
    )
    execution_time = models.FloatField(null=True, blank=True, verbose_name="Время выполнения (сек)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Решение {self.user.username} - {self.task.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Отправленное решение"
        verbose_name_plural = "Отправленные решения"


class Assignment(models.Model):
    """Модель назначения задачи конкретному классу (ДЗ / Классная работа)"""
    classroom = models.ForeignKey('accounts.Classroom', on_delete=models.CASCADE, related_name='assignments', verbose_name="Класс")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments', verbose_name="Задача")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн сдачи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата назначения")

    def __str__(self):
        return f"Задание '{self.task.title}' для класса '{self.classroom.name}'"

    class Meta:
        verbose_name = "Задание класса"
        verbose_name_plural = "Задания классов"


class CodeBattle(models.Model):
    """Модель дуэли 1 на 1 в реальном времени (Code Battle)"""
    class Status(models.TextChoices):
        WAITING = 'waiting', 'Ожидание соперника'
        IN_PROGRESS = 'in_progress', 'Идет битва'
        FINISHED = 'finished', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='battles', verbose_name="Задача")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_battles', verbose_name="Создатель")
    opponent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='joined_battles', verbose_name="Соперник")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_battles', verbose_name="Победитель")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.WAITING, verbose_name="Статус")
    creator_code = models.TextField(blank=True, default="", verbose_name="Код создателя")
    opponent_code = models.TextField(blank=True, default="", verbose_name="Код соперника")
    creator_passed = models.BooleanField(default=False, verbose_name="Создатель прошел тесты")
    opponent_passed = models.BooleanField(default=False, verbose_name="Соперник прошел тесты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Время старта")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Время завершения")

    def __str__(self):
        opp_name = self.opponent.username if self.opponent else 'Ожидание...'
        return f"Дуэль #{self.id}: {self.creator.username} vs {opp_name} [{self.get_status_display()}]"

    class Meta:
        verbose_name = "Code Battle Дуэль"
        verbose_name_plural = "Code Battle Дуэли"
        ordering = ['-created_at']


class TaskSolutionView(models.Model):
    """
    Фиксация того, что ученик сдался и посмотрел эталонный ответ к задаче.
    После этого за решение данной задачи ученик НЕ может получить опыт (XP) и достижения.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solution_views', verbose_name="Пользователь")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='solution_views', verbose_name="Задача")
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время просмотра")

    def __str__(self):
        return f"{self.user.username} посмотрел(а) ответ: {self.task.title}"

    class Meta:
        verbose_name = "Просмотр решения задачи"
        verbose_name_plural = "Просмотры решений задач"
        unique_together = ('user', 'task')