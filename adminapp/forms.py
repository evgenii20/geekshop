from django import forms

from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser

# получаем форму из authapp.forms для редактировани пользователя
from mainapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    # добавление дополнительного поля при редактировании категории в админке, initial=0 - по умолчанию
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        # Вместо атрибута разрешенных полей «fields» задаем «exclude» - кортеж с исключенными из отображения полями.
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
