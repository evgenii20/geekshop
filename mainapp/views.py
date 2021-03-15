import json
import os
# from datetime import datetime

# импортируем модуль с настройками
from django.conf import settings
# импортируем только файл, все переменные и константы
# from geekshop import settings
from django.shortcuts import render


# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
from mainapp.models import Product, ProductCategory


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:3]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    # описание url
    # links_menu = [
    #     {'href': 'products_all', 'name': 'все'},
    #     {'href': 'products_home', 'name': 'дом'},
    #     {'href': 'products_office', 'name': 'офис'},
    #     {'href': 'products_modern', 'name': 'модерн'},
    #     {'href': 'products_klassic', 'name': 'классика'},
    # ]
    title = 'Продукты'
    same_products = Product.objects.all()[:3]
    links_menu = ProductCategory.objects.all()
    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'о нас'
    # visit_date = datetime.now()
    # оставляем пустым
    locations = []
    # открываем JSON файл с объединением относительных путей и формируем структуру
    with open(os.path.join(settings.BASE_DIR, 'contacts.json'), encoding='utf-8') as f:
        locations = json.load(f)
    content = {'title': title, 'locations': locations}
    return render(request, 'mainapp/contact.html', content)
