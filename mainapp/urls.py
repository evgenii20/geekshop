"""mainapp URL products Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    # path('', mainapp.products, name='products'),
    path('', mainapp.products, name='index'),
    # re_path(r'^$', mainapp.products, name='index'),
    # используем для подгрузки категорий "<int:pk>/"
    # path('<int:pk>/', mainapp.products, name='category'),

    path('category/<int:pk>/', mainapp.products, name='category'),

    # re_path(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
    # третий уровень кеширования

    # re_path(r'^category/(?P<pk>\d+)/$', cache_page(3600)(mainapp.products)),

    # re_path(r'^category/(?P<pk>\d+)/ajax/$', cache_page(3600)(mainapp.products_ajax)),

    # один из вариантов написания передачи "page"
    # path('category/<int:pk>/<int:page>', mainapp.products, name='category'),
    # path('category/<int:pk>/<int:page>', mainapp.products, name='page'),

    # re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.product, name='page'),

    # re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/ajax/$', cache_page(3600)(mainapp.products_ajax)),

    # path('<int:pk>/', mainapp.products, name='category'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    # re_path(r'^product/(?P<pk>\d+)/$', mainapp.product, name='product'),

    # re_path(r'^category/(?P<pk>\d+)/$', mainapp.product, name='product'),

]
