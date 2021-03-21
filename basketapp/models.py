from django.conf import settings
from django.db import models

from mainapp.models import Product
# Create your models here.
# Второй шаг
# Третий makemigrations
# Четвёртый шаг migrate


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.PositiveSmallIntegerField(verbose_name='количество', default=0)
    # auto_now_add=True - при создании объекта, записывается дата
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    # class Meta:
    #     # На будущее, проверка связки 2-х полей на уникальность
    #     unique_together = ('user', 'product',)