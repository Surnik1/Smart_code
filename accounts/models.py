import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import date, timedelta


def generate_class_code():
    """Автоматическая генерация уникального 6-значного кода класса (например, X7K9P2)"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Ученик'
        TEACHER = 'teacher', 'Учитель'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.STUDENT, 
        verbose_name="Роль"
    )
    xp = models.PositiveIntegerField(default=0, verbose_name="Очки опыта (XP)")
    streak_days = models.PositiveIntegerField(default=0, verbose_name="Дней активности (Streak)")
    last_solve_date = models.DateField(null=True, blank=True, verbose_name="Дата последнего решения")

    @property
    def level_number(self) -> int:
        if self.xp < 3000:
            return 1
        elif self.xp < 10000:
            return 2
        elif self.xp < 40000:
            return 3
        elif self.xp < 100000:
            return 4
        elif self.xp < 500000:
            return 5
        elif self.xp < 1500000:
            return 6
        elif self.xp < 5000000:
            return 7
        elif self.xp < 10000000:
            return 8
        else:
            return 9 + (self.xp - 10000000) // 1000000

    @property
    def level_title(self) -> str:
        titles = {
            1: "Junior I",
            2: "Junior II",
            3: "Middle I",
            4: "Middle II",
            5: "Senior I",
            6: "Senior II",
            7: "Lead Developer",
            8: "Principal Engineer",
        }
        return titles.get(self.level_number, "Grandmaster")

    @property
    def progress_percent(self) -> int:
        brackets = [
            (0, 3000),
            (3000, 10000),
            (10000, 40000),
            (40000, 100000),
            (100000, 500000),
            (500000, 1500000),
            (1500000, 5000000),
            (5000000, 10000000),
        ]
        lvl = self.level_number
        if 1 <= lvl <= len(brackets):
            low, high = brackets[lvl - 1]
            return min(100, max(0, int(((self.xp - low) / (high - low)) * 100)))
        return 100

    def add_xp(self, amount: int):
        self.xp += amount
        self.save(update_fields=['xp'])

    def update_streak(self):
        today = date.today()
        if not self.last_solve_date:
            self.streak_days = 1
        elif self.last_solve_date == today:
            pass  # Уже решал сегодня
        elif self.last_solve_date == today - timedelta(days=1):
            self.streak_days += 1
        else:
            self.streak_days = 1  # Пропустил день, сброс на 1
        self.last_solve_date = today
        self.save(update_fields=['streak_days', 'last_solve_date'])

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()} | {self.level_title} | {self.xp} XP)"


class Achievement(models.Model):
    """Модель достижений платформы"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Код ачивки")
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    icon = models.CharField(max_length=50, default="trophy-fill", verbose_name="Иконка Bootstrap Icons")
    xp_reward = models.PositiveIntegerField(default=50, verbose_name="Награда XP")

    def __str__(self):
        return f"{self.title} (+{self.xp_reward} XP)"

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class UserAchievement(models.Model):
    """Связь пользователя с полученным достижением"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='awarded_users')
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата получения")

    class Meta:
        verbose_name = "Достижение пользователя"
        verbose_name_plural = "Достижения пользователей"
        unique_together = ('user', 'achievement')


# Сигнал для автоматического создания профиля при регистрации пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Classroom(models.Model):
    """Модель класса / группы"""
    name = models.CharField(max_length=255, verbose_name="Название класса / группы")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_classes', verbose_name="Учитель")
    code = models.CharField(max_length=10, unique=True, default=generate_class_code, verbose_name="Код класса")
    students = models.ManyToManyField(User, related_name='joined_classes', blank=True, verbose_name="Ученики")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.name} | Учитель: {self.teacher.username} (Код: {self.code})"

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"