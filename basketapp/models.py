from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


# Create your models here.
# Второй шаг
# Третий makemigrations
# Четвёртый шаг migrate

# # чтоб не пересекались с сигналами, комент
# class BasketQuerySet(models.QuerySet):
#     '''Менеджер объектов, для привязки к классу Basket необходимо указать
#     objects = BasketQuerySet.as_manager()'''
#
#     def delete(self, *args, **kwargs):
#         # Переопределяем метод delete, в self у нас лежит некий QuerySet(итерир-й объект) по которому мы можем пройтись
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         # super(BasketQuerySet, self).delete(*args, **kwargs)
#         # от родительского элемента удаление
#         super().delete()


class Basket(models.Model):
    # привязка менеджера объектов
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=0)
    # auto_now_add=True - при создании объекта, записывается дата
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    # class Meta:
    #     # На будущее, проверка связки 2-х полей на уникальность
    #     unique_together = ('user', 'product',)

    # @property
    # def product_cost(self):
    #     "return cost of all product this type"
    #     return self.product.price * self.quantity

    def _get_product_cost(self):
        # def product_cost(self):
        "return cost of all product this type"
        return self.product.price * self.quantity

    product_cost = property(_get_product_cost)
    # product_cost = cached_property(_get_product_cost, name='product_cost')

    @cached_property
    def get_items_cached(self):
        # "related_name='basket'" - указывается у того поля через которое мы будем ссылатся на эту модель
        # из поля "user" мы можем через "related_name='basket'" вытаскивать QuerySet "basket.select_related()"
        # таким образом:
        # _items = Basket.objects.filter(user=self.user) ранозначные вещи с:
        return self.user.basket.select_related()

    # @property
    # def total_quantity(self):
    def get_total_quantity(self):
        "return total quantity for user"
        # при каждом запросе идёт вычисление get_total_quantity
        # _items = Basket.objects.filter(user=self.user) заменяем на:
        _items = self.get_items_cached
        # list(map(lambda x: x.quantity, _items)) - получаем список из количества товаров всех корзинок конкретного
        # пользователя user=self.user; sum - суммируем количество
        # _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        # return _totalquantity
        return sum(list(map(lambda x: x.quantity, _items)))

    # total_quantity = property(_get_total_quantity)

    def get_total_cost(self):
        # при каждом запросе идёт вычисление get_total_quantity
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    @property
    def total_cost(self):
        # def get_total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_items(user):
        # передаём пользователя и получаем QuerySet 'product__category', к нему применяем метод delete в ordersapp views
        # return Basket.objects.filter(user=user).select_related()
        # return Basket.objects.filter(user=user).order_by('product__category')
        return user.basket.select_related().order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @staticmethod
    def get_item(pk):
        # return Basket.objects.get(pk=pk)
        return Basket.objects.get(pk=pk).first()

    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]

        return basket_items_dic

    # чтоб не пересекались с сигналами, комент
    # def delete(self):
    #     '''Метот относится к любому объекту в basket'''
    #     # тут работаем с одним объектом
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
