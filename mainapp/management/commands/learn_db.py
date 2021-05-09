from datetime import timedelta

from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from django.db import connection
from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from adminapp.views import db_profile_by_type

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#
#         home_query = Q(category__name='дом')
#         office_query = Q(category__name='офис')
#
#         # test_products = Product.objects.filter(
#         products = Product.objects.filter(
#             office_query | home_query
#         )
#
#         # print(len(test_products))
#         # print(len(products))
#         # print(test_products)
#         print(products)
#
#         # db_profile_by_type('learn db', '', connection.queries)
from ordersapp.models import OrderItem


class Command(BaseCommand):

    def handle(self, *args, **options):
        # константы
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        # временные промежутки
        action_1__time_delta = timedelta(hours=12)
        # 24 часа либо 1 день
        action_2__time_delta = timedelta(days=1)

        # скидка
        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        # условия, описываем условия фильтрации, через "__" обращаемся к методу "update", модификатор "lte" значит "<="
        # F('order__created') + action_1__time_delta - с времени заказа рошло не более 12 часов
        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        # с времени создания прошло "<=" 24 часа и строго больше чем 12 часов
        action_2__condition = Q(order__updated__lte=F('order__created') + action_2__time_delta) & \
                              Q(order__updated__gt=F('order__created') + action_1__time_delta)
        # с времени создания прошло строго больше чем дата создания + 24 часа
        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        # swith case SQL        условие             действие
        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)
        #                        условие                действие                                скидка
        action_1__price = When(action_1__condition, then=F('product__price') * F('quantity') * action_1__discount)
        #                        условие                действие                                скидка
        action_2__price = When(action_2__condition, then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        # test_orderss = OrderItem.objects.annotate(
        # annotate - добавление кастомного поля, на основе действий, SQL запроса
        orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                # если условия не покрывают всех случаев, то: default
                # default=ACTION_EXPIRED,
                output_field=IntegerField(),
            )
        ).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )
        ).order_by('action_order', 'total_price').select_related()

        # for orderitem in test_orderss:
        for orderitem in orders:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                   {orderitem.product.name:15}: скидка\
                   {abs(orderitem.total_price):6.2f} руб. | \
                   {orderitem.order.updated - orderitem.order.created}')
