import csv

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        with open("recipes/data/ingredients.csv", encoding="utf8") as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, units = row
                Ingredient.objects.get_or_create(name=name, units=units)
