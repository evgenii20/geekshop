import json
import os
# from datetime import datetime

# импортируем модуль с настройками
from django.conf import settings
# импортируем только файл, все переменные и константы
# from geekshop import settings
from django.shortcuts import render, get_object_or_404

# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:3]
    content = {'title': title, 'products': products}
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
    basket = []
    # basket = 0
    # если пользователь авторизован.    flat=True - прямой список
    if request.user.is_authenticated:
        # basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))
        basket = Basket.objects.filter(user=request.user)
        # альтернативный вариант получения корзины пользователя
        # _basket = request.user.basket.all()
        # print(f'basket / _basket: {len(_basket)} / {len(basket)}')

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
            'basket': basket
        }
        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[3:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'о нас'
    # visit_date = datetime.now()
    # оставляем пустым
    locations = []
    # открываем JSON файл с объединением относительных путей и формируем структуру
    with open(os.path.join(settings.BASE_DIR, 'mainapp/json/contact__locations.json'), encoding='utf-8') as f:
        locations = json.load(f)
    content = {'title': title, 'locations': locations}
    return render(request, 'mainapp/contact.html', content)
