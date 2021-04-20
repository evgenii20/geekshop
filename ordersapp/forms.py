from django import forms

from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # исключаем поле пользователя из отображения, поскольку с этим работает пользователь
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        # super(OrderForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class OrderItemForm(forms.ModelForm):
    # расширяем поля. Ставим "required=False" чтоб форма не требовала заполнения поля
    price = forms.CharField(label='Цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        # super(OrderItemForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
