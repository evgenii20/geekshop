from basketapp.models import Basket


def basket(request):
    print(f'context processor basket works')
    basket_list = []
    if request.user.is_authenticated:
        # basket_list = Basket.objects.filter(user=request.user)
        # basket_list = Basket.objects.filter(user=request.user).order_by('product__category')
        # basket = Basket.get_item(request.user)
        # basket_list = Basket.objects.filter(user=request.user).select_related()
        basket_list = Basket.objects.filter(user=request.user)
    return {
        'basket': basket_list
    }
