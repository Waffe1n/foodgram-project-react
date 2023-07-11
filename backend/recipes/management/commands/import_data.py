import csv

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Ingredient data import'

    def handle(self, *args, **options):
        with open(
            f'{settings.BASE_DIR}/static/data/ingredients.csv',
                encoding='utf-8') as f:
            '''Read as dict'''
            reader = csv.DictReader(f)
            Ingredient.objects.bulk_create(
                Ingredient(**content) for content in reader
            )

        self.stdout.write(self.style.SUCCESS('Данные загружены.'))
