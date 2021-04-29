from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from basketapp.models import Basket
from mainapp.models import Product

# CRUD
# Read
# @login_required(login_url='/auth/login/') - это не хорошо, url авторизации сменится и всё будет плохо
# во изежание этого задаём url в
@login_required
def basket(request):
    title = 'Корзина'
    # отсортированные корзинки пользователя по категории продукта
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

    content = {
        'title': title,
        'basket_items': basket_items
    }
    return render(request, 'basketapp/basket.html', content)

# Create
# Update
@login_required
def basket_add(request, pk):
    # reverse - преобразование записи namespace в обычный url, считаем что пользователь до авторизации пришёл
    # со страницы товара и редиректим его на страницу продукта
    # print(request.META.get('HTTP_REFERER'))
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    # Проверяем существующий товар, а не удалённый
    # product_item = get_object_or_404(Product, pk=pk)
    product = get_object_or_404(Product, pk=pk)

    # basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    # Анонимный пользователь не может использоваться как ключ и в нем нет ID, для авторизации пользователя
    # используется специальный декоратор @login_required
    # вариант блока представлен в коде ниже
    ## basket = Basket.objects.filter(user=request.user, product=product).first()
    # # if not basket_item:
    # if not basket:
    #     # basket_item = Basket(user=request.user, product=product_item)
    #     basket = Basket(user=request.user, product=product)
    #
    # # basket_item.quantity += 1
    # basket.quantity += 1
    # # basket_item.save()
    # basket.save()
    # # HTTP_REFERER - адрес откуда пришёл пользователь
    # # print(request.META.get('HTTP_REFERER'))
    ## return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    old_basket_item = Basket.get_product(user=request.user, product=product).select_related()
    if old_basket_item:
        old_basket_item[0].quantity += 1
        old_basket_item[0].save()
    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity += 1
        # для django 3-й или выше версии с "update_fields=['quantity', 'product']", в др. случ. пусто ".save()"
        # new_basket_item.save(update_fields=['quantity', 'product'])
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# CBV
# @login_required
# class BasketUpdateView(UpdateView):
#     model = Basket
#     product_item = get_object_or_404(Product, pk=['pk'])
#     # 1-метод получения
#     # def get_queryset(self):
#     #     # альтернатива строчке "old_basket_item = Basket.get_product(user=request.user, product=product)"
#     #     basket_item = Basket.objects.filter(user=self.request.user, product__pk=self.kwargs['pk']).first()
#     #     if not basket_item:
#     #         basket_item = Basket.objects.create(user=self.request.user, product__pk=self.kwargs['pk'])
#     #     return Basket.objects.filter(user=self.request.user, product__pk=self.kwargs['pk'])
#
#     # 2-метод получения
#     def get_object(self, **kwargs):
#         '''Получение object'''
#         # альтернатива строчке "old_basket_item = Basket.get_product(user=request.user, product=product)"
#         basket_item = Basket.objects.filter(user=self.request.user, product__pk=self.kwargs['pk']).first()
#         if not basket_item:
#             basket_item = Basket.objects.create(user=self.request.user, product__pk=self.kwargs['pk'])
#         basket_item.quantity += 1
#         basket_item.save()
#         return basket_item
#
#     def form_valid(self, form):
#         if 'login' in self.request.META.get('HTTP_REFERER'):
#             return HttpResponseRedirect(reverse('products:product', args=['pk']))
#         return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         # метод dispatch отвечает за контроль авторизации, но только при
#         # @method_decorator(user_passes_test(lambda u: u.is_superuser))
#         return super().dispatch(*args, **kwargs)


# Delete
@login_required
def basket_remove(request, pk):
    # проверяем существование корзины, если нет|ошибка, если да|удаляем
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    # возвращаем пользователя на исходную страницу с которой он пришёл
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            # Если количество товара стало равно нулю — удаляем его из корзины.
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

        content = {
            'basket_items': basket_items,
        }
        # тот же самый render только не передаётся request, а передаётся шаблон в виде строки текста
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})