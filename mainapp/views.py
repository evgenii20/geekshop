from datetime import datetime

from django.shortcuts import render


# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
def main(request):
    content = {
        'title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    # описание url
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_klassic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', content)
