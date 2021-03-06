from django.shortcuts import render

# Create your views here.
# Принимаем запросы от пользователей "request" и возвращаем "request" чтоб не потерять цепочку запросов
def main(request):
    return render(request, 'mainapp/index.html')

def products(request):
    return render(request, 'mainapp/products.html')

def contact(request):
    return render(request, 'mainapp/contact.html')