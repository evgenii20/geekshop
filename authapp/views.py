from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm

# Create your views here.
from authapp.models import ShopUser

#@csrf_exempt
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
            # register_form.save()
            user = register_form.save()
            if send_verify_email(user):
                print('success')
            else:
                print('failed')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', content)

@login_required
def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        # instance=request.user - указывает на тот объект который мы редактируем
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        # Добавим ещё одну форму
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            # profile_form - сохраняется через сигналы, поэтому сохранение тут отсутствует
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        # если GET запрос
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'authapp/edit.html', content)

def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    # title = f'Подтверждение учетной записи {user.username}'
    subject = f'Подтверждение учетной записи {user.username}'

    # message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME}\
    #  перейдите по ссылке:\n{settings.DOMAIN_NAME}\n{verify_link}'

    # в verify_link допишется "/"
    message = f'Ссылка для активации: {settings.BASE_URL}{verify_link}'

    # return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
    #          Тема             сообщение   от кого               кому список   флаг ошибки
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)

def veryfy(request, email, activation_key):
    user = ShopUser.objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        user.is_active = True
        # для запрета повторных активаций пользователя "user.activation_key = ''"
        user.activation_key = ''
        user.save()
        # Если с пользователем всё хорошо, то логиним, если нет, то анонимный пользователь
        # не попадает в это условие и видит текст на странице "verification.html"
        auth.login(request, user)
    return render(request, 'authapp/verification.html')
