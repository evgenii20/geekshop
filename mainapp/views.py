import json
import os
# from datetime import datetime

# импортируем модуль с настройками
import random

from django.conf import settings
from django.core.cache import cache
# импортируем только файл, все переменные и константы
# from geekshop import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page, never_cache

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

JSON_PATH = 'mainapp/json'


# --- cache
# первый уровень кеширования
def get_links_menu():
    # проверка низкоуровнего кеширования
    if settings.LOW_CACHE:
        # генерируем ключ
        key = 'links_menu'
        # забираем данные из кэша по ключу
        links_menu = cache.get(key)
        # если это 1-й запрос к кэшу
        if links_menu is None:
            # если в кэше нет данных, заполняем из БД
            links_menu = ProductCategory.objects.filter(is_active=True).select_related()
            # вносим в кэш для повторных обращений
            cache.set(key, links_menu)
            return links_menu
    else:
        # если LOW_CACHE = False, выводим список из БД
        return ProductCategory.objects.filter(is_active=True).select_related()


def get_category(pk):
    if settings.LOW_CACHE:
        # генерируем ключ для каждой из категорий
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            # category = ProductCategory.objects.get(pk=pk) или
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by(
                'price').select_related()
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price').select_related()


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price').select_related()
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
            'price').select_related()


# ---/ cache


def load_from_json(file_name):
    '''Функция загрузки json'''
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore', encoding='utf-8') as infile:
        return json.load(infile)


def get_hot_product():
    "горячее предложение"
    # products = Product.objects.all()
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related()
    # products = Product.objects.filter(category__is_active=True).select_related()
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
    # до кэша:
    # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    # после:
    products = get_products()[:3]
    # products = Product.objects.filter(is_active=True, category__is_active=True)[:3]

    content = {
        'title': title,
        'products': products
    }

    return render(request, 'mainapp/index.html', content)



# @never_cache
# @cache_page(3600)
def products(request, pk=None):
    # def products(request, pk=None, page=1):
    # только для продукта
    title = 'Продукты'
    # links_menu = ProductCategory.objects.all()
    # is_active=True - не показывать скрытые, .select_related()
    # до кэша:
    # links_menu = ProductCategory.objects.filter(is_active=True).select_related()
    # после кэша: применение низкоуровнего кеширования
    links_menu = get_links_menu()

    # при def products(request, pk=None):
    page = request.GET.get('p', 1)

    # при def products(request, pk=None):
    # if pk is not None:

    if pk:
        if pk == 0:
            # категория товара на странице продукта
            # category_item = {'name': 'все', 'pk': 0}
            category = {'pk': 0, 'name': 'все'}
            # category = {'pk': get_category(pk=0), 'name': 'все'}

            # products = Product.objects.all().order_by('price')
            # products = Product.objects.filter(is_active=True, category__is_active=True).order_by(
            # products = get_links_menu().order_by(
            # до кэша:
            # products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price').select_related()
            # после:
            products = get_products_ordered_by_price()
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk=pk)
            # если не 404, то выбираем объекты
            # до кэша:
            # products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
            #   order_by('price')
            # после:
            products = get_products_in_category_ordered_by_price(pk)
            # products_list = Product.objects.filter(category=

        # постраничный вывод
        # paginator = Paginator(products, 2)
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
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', content)


# клон
# def products_ajax(request, pk=None, page=1):
#     if request.is_ajax():
#         links_menu = get_links_menu()
#
#         if pk:
#             if pk == '0':
#                 category = {
#                     'pk': 0,
#                     'name': 'все'
#                 }
#                 products = get_products_ordered_by_price()
#             else:
#                 category = get_category(pk)
#                 products = get_products_in_category_ordered_by_price(pk)
#
#             paginator = Paginator(products, 2)
#             try:
#                 products_paginator = paginator.page(page)
#             except PageNotAnInteger:
#                 products_paginator = paginator.page(1)
#             except EmptyPage:
#                 products_paginator = paginator.page(paginator.num_pages)
#
#             content = {
#                 'links_menu': links_menu,
#                 'category': category,
#                 'products': products_paginator,
#             }
#
#             result = render_to_string(
#                 'mainapp/includes/inc_products_list_content.html',
#                 context=content,
#                 request=request)
#
#             return JsonResponse({'result': result})


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


# до кэша:
# def contact(request):
#     title = 'о нас'
#     # visit_date = datetime.now()
#     # оставляем пустым
#     # locations = []
#     locations = load_from_json('contact__locations')
#     # открываем JSON файл с объединением относительных путей и формируем структуру, для оптимизации вынесем в функцию
#     # load_from_json('')
#     # with open(os.path.join(settings.BASE_DIR, 'mainapp/json/contact__locations.json'), encoding='utf-8') as f:
#     #     locations = json.load(f)
#     content = {
#         'title': title,
#         'locations': locations,
#     }
#     return render(request, 'mainapp/contact.html', content)
# после:
def contact(request):
    title = 'о нас'
    if settings.LOW_CACHE:
        key = f'locations'
        locations = cache.get(key)
        if locations is None:
            locations = load_from_json('contact__locations')
            cache.set(key, locations)
    else:
        locations = load_from_json('contact__locations')

    content = {
        'title': title,
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)
