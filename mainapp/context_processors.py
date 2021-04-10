from basketapp.models import Basket


def basket(request):
    print(f'context processor basket works')
    basket_list = []
    if request.user.is_authenticated:
        basket_list = Basket.objects.filter(user=request.user)
    return {
        'basket': basket_list
    }
