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
    @property
    def product_cost(self):
        "return cost of all product this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        _items = Basket.objects.filter(user=self.user)
        # list(map(lambda x: x.quantity, _items)) - получаем список из количества товаров всех корзинок конкретного
        # пользователя user=self.user; sum - суммируем количество
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost