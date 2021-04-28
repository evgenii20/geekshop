import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        '''Фильтруем заказы по текущему пользователю'''
        return Order.objects.filter(user=self.request.user).select_related()

    # @method_decorator(login_required())
    # def dispatch(self, *args, **kwargs):
    #     return super(ListView, self).dispatch(*args, **kwargs)


# OrderItemsCreate
class OrderCreateView(CreateView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')
    # Выводит поле выбора статуса
    # form_class = OrderForm
    fields = []

    def get_context_data(self, **kwargs):
        # data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        data = super().get_context_data(**kwargs)

        # FormSet - набор форм, зависит от основной формы и ссылается на FormSet
        # OrderFormSet - просто переменная. Осн-я, второст-я модель,  форма,      количество строк для вывода в форму
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            # Если else, собираем formset пустой
            # basket_items = Basket.get_items(self.request.user)
            # Выбираем все корзины пользователя
            basket_items = Basket.objects.filter(user=self.request.user).select_related()
            if len(basket_items):
                # Переносим в заказ, extra=len(basket_items)
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                # form - хранит инфо о свободных местах из extra=len(basket_items)
                for num, form in enumerate(formset.forms):
                    # заполняем данными, для 5 корзин - 5 заказов
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    # заполняем поле цена указанное в forms
                    form.initial['price'] = basket_items[num].product.price

            else:
                formset = OrderFormSet()
            # после заполнения и передачи на обработку нам эти данные не нужны, удаляем
            # basket_items.delete()

        # передаём formset дальше
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        '''Сохраняем formset вызываемый при POST запросе к контроллеру OrderCreateView'''
        # выбираем весь контекст, набор форм и пользовательский ввод
        context = self.get_context_data()
        orderitems = context['orderitems']

        # исключаем возможность ввода ошибочной информации от пользователя при передаче формы,
        # если is_valid - false, orderitems не сохраняется
        # для избежания этого оборачиваем код в атомарную(не делима) транзакцию к БД
        with transaction.atomic():
            # а тут delete() применяем к QuerySet с корзинами пользователя
            Basket.get_items(self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                # instance - ссылка на родительский класс
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


# OrderRead
class OrderDetailView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'заказ/просмотр'
        return context


class OrderUpdateView(UpdateView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')
    # Выводит поле выбора статуса
    # form_class = OrderForm
    fields = []

    def get_context_data(self, **kwargs):
        # data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        data = super().get_context_data(**kwargs)

        # FormSet - набор форм, зависит от основной формы и ссылается на FormSet
        # OrderFormSet - просто переменная. Осн-я, второст-я модель,  форма,      количество строк для вывода в форму
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            # data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            # data['orderitems'] = OrderFormSet(instance=self.object)
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            # data['orderitems'] = formset
        # передаём formset дальше
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        '''Сохраняем formset вызываемый при POST запросе к контроллеру OrderCreateView'''
        # выбираем весь контекст, набор форм и пользовательский ввод
        context = self.get_context_data()
        orderitems = context['orderitems']

        # исключаем возможность ввода ошибочной информации от пользователя при передаче формы,
        # если is_valid - false, orderitems не сохраняется
        # для избежания этого оборачиваем код в атомарную(не делима) транзакцию к БД
        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                # instance - ссылка на родительский класс
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    # Метод удаления переопределён в модели Order, поэтому дополнительно ничего не пишем
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


# совершение покупки
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

# сигналы, можно на одну функцию 2 сигнала
@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    '''Обновление при сохранении'''
    # one случай
    # если у нас поля которые были обновлены 'quantity' or 'product', то мы должны понять, это создание или обновление
    # когда идёт pre_save мы ещё ничего не сохранили в базу, т.к. не сохранили у нас нет "pk" а запись находится
    # в instance значит делаем проверку "if"
    # if update_fields in  :
    if update_fields is 'quantity' or 'product':
        # default instance.pk = None
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            # если продукт новый
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    '''Обновление при удалении'''
    # two случай
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            # возврат данных в виде "JsonResponse" для удачной сериализации в дальнейшем
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})