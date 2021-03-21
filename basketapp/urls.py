from django.urls import path

from basketapp import views as basketapp

# Пятый шаг
# Шестой шаг (включить в geekshop\urls)
# Влияет на namespace
app_name = 'basketapp'

urlpatterns = [
    # Read
    path('', basketapp.basket, name='view'),
    # Create
    # Update
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    # Delete
    path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit')
]
