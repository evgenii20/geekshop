from django.conf import settings
from django.db import models


# Create your models here.
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    # ORDER_STATUSES
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # auto_now_add=True - заполняется при создании записи
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    # auto_now=True - фиксация даты при любых изменениях записи
    updated = models.DateTimeField(verbose_name='изменён', auto_now=True)
    # choices - выбор, max_length=3 - это PROCEEDED = 'PRD'
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    # флаг удаления, по умолчанию активен
    is_active = models.BooleanField(db_index=True, verbose_name='активен', default=True)

    class Meta:
        # сортировка для CBV, по умолчанию от более новых к старым заказам (кортеж,):
        ordering = ('-created',)
        # имя класса в единственном числе:
        verbose_name = 'заказ'
        # имя класса во множественном числе:
        verbose_name_plural = 'заказы'

    def __str__(self):
        # return 'Текущий заказ: {}'.format(self.id)
        return f'Текущий заказ: {self.pk}'

    def get_total_quantity(self):
        # при помощи метода «select_related()» находим все элементы заказа
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        # return sum(list(map(lambda x: x.quantity * x.product.price, items)))
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    # переопределяем метод, удаляющий объект is_active
    def delete(self):
        for item in self.orderitems.select_related():
            # и корректируем количество продуктов на складе (возвращаем на склад)
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    '''Раскладываем корзину заказов на отдельные продукты'''
    # от каждого объекта через точку сможем получить доступ к "orderitems"
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        # Количество и продукт теперь в OrderItem, поэтому сдесь делаем подсчёт стоимости
        return self.product.price * self.quantity
