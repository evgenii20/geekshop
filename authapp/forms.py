from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        # Раскладываем словарь, form-control - от bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']

        # для проектов с низкой нагрузкой !>й
        # if ShopUser.objects.filter(email=data).count() > 0:
        #     f"""select count(*) from authapp_shopuser where email={data}"""
        #     pass # raise ...
        # f"""select count(1) from authapp_shopuser where email={data}"""

        # users_emails = ShopUser.objects.values_list('email', flat=True)
        # users_emails = list(ShopUser.objects.values_list('email', flat=True))
        # if data in users_emails: из базы
        if ShopUser.objects.filter(email=data).exists():
            raise forms.ValidationError("Email exists")
        return data


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                # HiddenInput() - прячем поле с паролем:
                field.widget = forms.HiddenInput()

    def clean_age(self):
        # self.cleaned_data['age'] - лежит то, что нам передал пользователь
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        # exists из SQL
        if ShopUser.objects.filter(email=data).exists():
            raise forms.ValidationError("Email exists")
        return data