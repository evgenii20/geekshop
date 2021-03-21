from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


# Create your views here.
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    # content = {}
    # return render(request, 'basketapp/basket.html', content)
    pass

# Create
# Update
def basket_add(request, pk):
    # Проверяем существующий товар, а не удалённый
    # product_item = get_object_or_404(Product, pk=pk)
    product = get_object_or_404(Product, pk=pk)
    # basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    basket = Basket.objects.filter(user=request.user, product=product).first()
    # if not basket_item:
    if not basket:
        # basket_item = Basket(user=request.user, product=product_item)
        basket = Basket(user=request.user, product=product)

    # basket_item.quantity += 1
    basket.quantity += 1
    # basket_item.save()
    basket.save()
    # HTTP_REFERER - адрес откуда пришёл пользователь
    # print(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    # content = {}
    # return render(request, 'basketapp/basket.html', content)
    pass
