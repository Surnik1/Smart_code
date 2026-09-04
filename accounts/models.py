import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# Сигналы для автоматического создания профиля при регистрации пользователя
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()


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