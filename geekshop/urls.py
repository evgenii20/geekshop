"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from mainapp import views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    # path('products/', mainapp.products, name='products'),
    # include all url is mainapp.urls, т.е. в каждом приложении свои URL, namespace='products' - для использования URL
    path('products/', include('mainapp.urls', namespace='products')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('contact/', mainapp.contact, name='contact'),

    # ссылка на стандартную админку, переименуем в "control/" для добавления своей админки ниже
    # path('admin/', admin.site.urls),
    # path('control/', admin.site.urls),

    # своя админка namespace='admins' - исключаем конфликт
    # с использованием регулярных выражений re_path для сложных проектов
    # re_path(r'^admin/', include('adminapp.urls', namespace='admin'))
    path('admin/', include('adminapp.urls', namespace='admin')),
    # добавляем модуль "social_django"
    path('', include('social_django.urls', namespace='social')),
    # re_path(r'^order/', include('ordersapp.urls', namespace='order')),
    path('order/', include('ordersapp.urls', namespace='order'))
]

# настройка работает локально
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # подгрузка toolbar
# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
