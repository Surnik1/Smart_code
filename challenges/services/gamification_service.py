from datetime import datetime
from typing import Dict, Any, List
from django.contrib.auth import get_user_model
from accounts.models import Profile, Achievement, UserAchievement
from challenges.models import Task, Submission

User = get_user_model()

DEFAULT_ACHIEVEMENTS = [
    {
        "code": "first_blood",
        "title": "Первая кровь",
        "description": "Решил свою первую задачу на платформе Smart Code!",
        "icon": "award-fill",
        "xp_reward": 50,
    },
    {
        "code": "streak_3",
        "title": "Огненный старт 🔥",
        "description": "Решал задачи 3 дня подряд без перерыва!",
        "icon": "fire",
        "xp_reward": 100,
    },
    {
        "code": "streak_7",
        "title": "Неудержимый ⚡",
        "description": "Учебный стрик 7 дней подряд!",
        "icon": "lightning-charge-fill",
        "xp_reward": 250,
    },
    {
        "code": "five_tasks",
        "title": "Алгоритмист I",
        "description": "Успешно решил 5 уникальных задач!",
        "icon": "code-slash",
        "xp_reward": 150,
    },
    {
        "code": "ten_tasks",
        "title": "Алгоритмист II",
        "description": "Успешно решил 10 уникальных задач!",
        "icon": "cpu-fill",
        "xp_reward": 300,
    },
    {
        "code": "night_owl",
        "title": "Ночной кодер 🌙",
        "description": "Сдал рабочее решение глубокой ночью (с 00:00 до 05:00)!",
        "icon": "moon-stars-fill",
        "xp_reward": 50,
    },
    {
        "code": "battle_winner",
        "title": "Гладиатор ⚔️",
        "description": "Одержал победу в дуэли Code Battle 1 на 1!",
        "icon": "shield-fill-check",
        "xp_reward": 100,
    },
]


class GamificationService:
    """Сервис геймификации, начисления опыта, обновления стрика и выдачи достижений"""

    @classmethod
    def seed_achievements(cls):
        """Гарантирует существование базовых достижений в базе данных"""
        for item in DEFAULT_ACHIEVEMENTS:
            Achievement.objects.get_or_create(
                code=item["code"],
                defaults={
                    "title": item["title"],
                    "description": item["description"],
                    "icon": item["icon"],
                    "xp_reward": item["xp_reward"],
                }
            )

    @classmethod
    def award_achievement(cls, user, code: str) -> bool:
        """Выдает ачивку пользователю, если она еще не была получена, и начисляет бонусный XP"""
        cls.seed_achievements()
        try:
            achievement = Achievement.objects.get(code=code)
        except Achievement.DoesNotExist:
            return False

        user_ach, created = UserAchievement.objects.get_or_create(
            user=user,
            achievement=achievement,
        )
        if created:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.add_xp(achievement.xp_reward)
            return True
        return False

    @classmethod
    def on_task_passed(cls, user, task: Task, submission: Submission = None) -> Dict[str, Any]:
        """
        Вызывается при успешном прохождении всех тестов задачи.
        Начисляет XP (если задача решается впервые), обновляет стрик и проверяет ачивки.
        """
        cls.seed_achievements()
        profile, _ = Profile.objects.get_or_create(user=user)

        # 1. Проверяем, решалась ли эта задача пользователем ранее
        sub_query = Submission.objects.filter(user=user, task=task, status=Submission.Status.PASSED)
        if submission and submission.id:
            sub_query = sub_query.exclude(id=submission.id)
        already_solved = sub_query.exists()

        xp_earned = 0
        if not already_solved:
            difficulty_xp = {
                Task.Difficulty.EASY: 50,
                Task.Difficulty.MEDIUM: 100,
                Task.Difficulty.HARD: 200,
            }
            xp_earned = difficulty_xp.get(task.difficulty, 50)
            profile.add_xp(xp_earned)

        # 2. Обновляем Daily Streak
        profile.update_streak()

        # 3. Проверяем достижения
        new_achievements: List[str] = []

        # Первая кровь (первая решенная задача)
        solved_count = (
            Submission.objects.filter(user=user, status=Submission.Status.PASSED)
            .values('task')
            .distinct()
            .count()
        )
        if solved_count >= 1:
            if cls.award_achievement(user, "first_blood"):
                new_achievements.append("Первая кровь (+50 XP)")

        # 5 и 10 задач
        if solved_count >= 5:
            if cls.award_achievement(user, "five_tasks"):
                new_achievements.append("Алгоритмист I (+150 XP)")
        if solved_count >= 10:
            if cls.award_achievement(user, "ten_tasks"):
                new_achievements.append("Алгоритмист II (+300 XP)")

        # Стрик 3 и 7 дней
        if profile.streak_days >= 3:
            if cls.award_achievement(user, "streak_3"):
                new_achievements.append("Огненный старт 🔥 (+100 XP)")
        if profile.streak_days >= 7:
            if cls.award_achievement(user, "streak_7"):
                new_achievements.append("Неудержимый ⚡ (+250 XP)")

        # Ночной кодер (с 00:00 до 05:00)
        current_hour = datetime.now().hour
        if 0 <= current_hour < 5:
            if cls.award_achievement(user, "night_owl"):
                new_achievements.append("Ночной кодер 🌙 (+50 XP)")

        profile.refresh_from_db()

        return {
            "xp_earned": xp_earned,
            "total_xp": profile.xp,
            "level_title": profile.level_title,
            "level_number": profile.level_number,
            "streak_days": profile.streak_days,
            "new_achievements": new_achievements,
        }

