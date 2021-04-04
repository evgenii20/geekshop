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

from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    # path('', mainapp.products, name='products'),
    path('', mainapp.products, name='index'),
    # используем для подгрузки категорий "<int:pk>/"
    # path('<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/', mainapp.products, name='category'),
    # один из вариантов написания передачи "page"
    # path('category/<int:pk>/<int:page>', mainapp.products, name='category'),
    # path('category/<int:pk>/<int:page>', mainapp.products, name='page'),
    # path('<int:pk>/', mainapp.products, name='category'),
    path('product/<int:pk>/', mainapp.product, name='product'),
]
