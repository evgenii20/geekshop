import json
import os
# from datetime import datetime

# импортируем модуль с настройками
import random

from django.conf import settings
# импортируем только файл, все переменные и константы
# from geekshop import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    '''Функция загрузки json'''
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore', encoding='utf-8') as infile:
        return json.load(infile)


def get_hot_product():
    "горячее предложение"
    # products = Product.objects.all()
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related()
    # возврат 1 случайного продукта из списка
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    "похожие продукты"
    # берём 3 похожих продукта из горячей категории и исключаем(exclude) текущий из выборки
    same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    # products = Product.objects.all()[:3]
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    # products = Product.objects.filter(is_active=True, category__is_active=True)[:3]

    content = {
        'title': title,
        'products': products
    }

    return render(request, 'mainapp/index.html', content)


# def products(request, pk=None, page=1):
def products(request, pk=None):
    # только для продукта
    title = 'Продукты'
    # links_menu = ProductCategory.objects.all()
    # is_active=True - не показывать скрытые, .select_related()
    links_menu = ProductCategory.objects.filter(is_active=True).select_related()

    page = request.GET.get('p', 1)

    if pk is not None:
        if pk == 0:
            # products = Product.objects.all().order_by('price')
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price').select_related()
            # категория товара на странице продукта
            # category_item = {'name': 'все', 'pk': 0}
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            # если не 404, то выбираем объекты
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).\
                order_by('price')
            # products_list = Product.objects.filter(category=

        # постраничный вывод
        paginator = Paginator(products, 2)
        # обработка ошибок
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            # 'category': category_item,
            # 'products': products,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', content)

    # same_products = Product.objects.all()[3:5]
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    "Передаём объект продукта, полученный по pk в шаблон"
    title = 'продукт'
    # links_menu
    # product

    content = {
        'title': title,
        # QuerySet
        # 'links_menu': ProductCategory.objects.all(),
        'links_menu': ProductCategory.objects.filter(is_active=True).select_related(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'о нас'
    # visit_date = datetime.now()
    # оставляем пустым
    # locations = []
    locations = load_from_json('contact__locations')
    # открываем JSON файл с объединением относительных путей и формируем структуру, для оптимизации вынесем в функцию
    # load_from_json('')
    # with open(os.path.join(settings.BASE_DIR, 'mainapp/json/contact__locations.json'), encoding='utf-8') as f:
    #     locations = json.load(f)
    content = {
        'title': title,
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)
