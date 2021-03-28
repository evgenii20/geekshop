import json
import os
# from datetime import datetime

# импортируем модуль с настройками
import random

from django.conf import settings
# импортируем только файл, все переменные и константы
# from geekshop import settings
from django.shortcuts import render, get_object_or_404

# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

def get_basket(user):
    # if request.user.is_authenticated:
    # если пользователь авторизован "user.is_authenticated",
    if user.is_authenticated:
        # то возвращаем QuerySet, иначе [] - пустой список
        return Basket.objects.filter(user=user)
        # альтернативный вариант получения корзины пользователя
        # _basket = request.user.basket.all()
        # print(f'basket / _basket: {len(_basket)} / {len(basket)}')
    return []

def get_hot_product():
    "горячее предложение"
    products = Product.objects.all()
    # возврат 1 случайного продукта из списка
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    "похожие продукты"
    # берём 3 похожих продукта из горячей категории и исключаем(exclude) текущий из выборки
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:3]
    # content = {'title': title, 'products': products}
    content = {'title': title, 'products': products, 'basket': get_basket(request.user)}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    # print(pk)
    # описание url
    # links_menu = [
    #     {'href': 'products_all', 'name': 'все'},
    #     {'href': 'products_home', 'name': 'дом'},
    #     {'href': 'products_office', 'name': 'офис'},
    #     {'href': 'products_modern', 'name': 'модерн'},
    #     {'href': 'products_klassic', 'name': 'классика'},
    # ]
    # только для продукта
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            # products_list = Product.objects.all().order_by('price').select_related()
            products = Product.objects.all().order_by('price')
            # категория товара на странице продукта
            # category_item = {'name': 'все', 'pk': 0}
            category = {'name': 'все'}
            # report = []
            # for prod in products_list:
            #     report.append({
            #         'category': prod.category.name,
            #         'price': prod.price
            #     })
        else:
            # Не совсем верный вариант
            # category_item = ProductCategory.objects.filter(pk=pk).first()
            # if not category_item:
            #     raise ...
            # category_item = ProductCategory.objects.get(pk=pk)
            #                                   модель, условие
            category = get_object_or_404(ProductCategory, pk=pk)
            # если не 404, то выбираем объекты
            products = Product.objects.filter(category__pk=pk).order_by('price')
            # products_list = Product.objects.filter(category=category_item)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            # 'category': category_item,
            'products': products,
            # 'products': products_list,
            # 'hot_product': hot_product,
            # 'same_products': same_products,
            # 'basket': get_basket(request.user)
            'basket': basket
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
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)

def product(request, pk):
    "Передаём объект продукта, полученный по pk в шаблон"
    title = 'продукт'

    content = {
        'title': title,
        # QuerySet
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)

def contact(request):
    title = 'о нас'
    # visit_date = datetime.now()
    # оставляем пустым
    locations = []
    # открываем JSON файл с объединением относительных путей и формируем структуру
    with open(os.path.join(settings.BASE_DIR, 'mainapp/json/contact__locations.json'), encoding='utf-8') as f:
        locations = json.load(f)
    content = {'title': title, 'locations': locations, 'basket': get_basket(request.user)}
    return render(request, 'mainapp/contact.html', content)
