from django.core.management.base import BaseCommand
from challenges.services.gamification_service import GamificationService


class Command(BaseCommand):
    help = 'Создаёт базовые достижения (ачивки) в базе данных, если они ещё не существуют.'

    def handle(self, *args, **options):
        GamificationService.seed_achievements()
        self.stdout.write(self.style.SUCCESS('✅ Базовые достижения успешно созданы / проверены.'))
