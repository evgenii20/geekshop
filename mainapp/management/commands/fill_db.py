import json
import os

from django.conf import settings
# from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    '''Функция загрузки JSON файла'''
    with open(os.path.join(settings.BASE_DIR, f'mainapp/json/{file_name}.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):

    def handle(self, *args, **option):
        categories = load_from_json('categories')
        # print(categories)

        # Удаление всей таблицы категорий
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)
            # **cat: 'name': 'дом', 'description': 'Отличная мебель для домашнего интерьера.'

        products = load_from_json('products')
        # Удаление продуктов
        Product.objects.all().delete()
        # выборка из базы
        for prod in products:
            _cat = ProductCategory.objects.get(name=prod['category'])
            prod['category'] = _cat
            Product.objects.create(**prod)

        # Создадим пользователя
        ShopUser.objects.create_superuser('django', 'django@local.gb', 'geekbrains', age=30)

