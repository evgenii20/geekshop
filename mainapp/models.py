from django.db import models


# Create your models here.
class ProductCategory(models.Model):
    # При необходимости поле id можно задать в ручную, BigAutoField - для больших значений
    # id = models.BigAutoField(primary_key=True)
    # категории товара = тип товара, поля
    # name - обязательное для заполнения поле
    name = models.CharField(max_length=64, unique=True, verbose_name='имя')
    # описание, если blank=True, то это поле может оставаться пустым и оно не обязательное
    description = models.TextField(verbose_name='описание', blank=True)
    # флаг удаления, не удаляя полностью
    is_active = models.BooleanField(verbose_name='активность', default=True)

    def __str__(self):
        # '''Преобразование объекта к строке'''
        return self.name


# Один ко многим. models подключается из django.db
class Product(models.Model):
    # "on_delete=" - что делать при удалении? on_delete=models.SET_NULL, blank=True, null=True
    # blank=True и null=True чаще идут в паре и указывают на необязательность заполнения поля
    # models.CASCADE() - каскадное удаление записи из всех таблиц
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='имя')
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=64, verbose_name='краткое описание', blank=True)
    description = models.TextField(blank=True, verbose_name='описание')
    # "max_digits=8" - кол-во знаков до ",", "decimal_places=2" - после
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активность', default=True)
    # is_active = models.BooleanField(db_index=True, verbose_name='активность', default=True)

    def __str__(self):
        # '''Строковое отображение'''
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_items():
        # '''Убираем неактивные продукты с формы'''
        return Product.objects.filter(is_active=True).order_by('category', 'name')
