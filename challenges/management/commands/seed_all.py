from django.core.management.base import BaseCommand
from scripts.seed_all import run_seeder


class Command(BaseCommand):
    help = 'Создаёт и обновляет все задачи (129 шт), тесты (>=10 на задачу), достижения и суперпользователя в базе данных.'

    def handle(self, *args, **options):
        run_seeder(stdout=self.stdout, style=self.style)
