import datetime

from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from basketapp.models import Basket
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        '''Фильтруем заказы по текущему пользователю'''
        return Order.objects.filter(user=self.request.user)


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
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                # Переносим в заказ, extra=len(basket_items)
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                # form - хранит инфо о свободных местах из extra=len(basket_items)
                for num, form in enumerate(formset.forms):
                    # заполняем данными, для 5 корзин - 5 заказов
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity

            else:
                formset = OrderFormSet()
            # после заполнения и передачи на обработку нам эти данные не нужны, удаляем
            basket_items.delete()

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

