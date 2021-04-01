from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm


# Create your views here.


def login(request):
    title = 'вход'
    # POST - при отправке форм, авторизации
    # login_form = ShopUserLoginForm(data=request.POST)
    login_form = ShopUserLoginForm(data=request.POST or None)

    # http://127.0.0.1:8000/auth/login/?next=/basket/add/5/
    # next = request.GET.get('next', '') - упрощённая запись варианта ниже:
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        # При использовании не обязательных полей, можно себя обезопасить передав метод "get"
        # с вторым параметром "None", например "username = request.POST.get('username', None)"
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            # передали next из формы стандартной авторизации в пост запросе скрытого инпута
            if 'next' in request.POST.keys():
                # print('redirect next', request.POST['next'])
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    # request.FILES - все поля формы которые относятся к загрузке файлов
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        # instance=request.user - указывает на тот объект который мы редактируем
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', content)
