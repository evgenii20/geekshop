from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):
    SUCCESS_STATUS_CODE = 200
    ERROR_STATUS_CODE = 500

    def setUp(self):
        '''Для установки данных, записи данных в БД и внутренних преобразований'''
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        # self.client = Client()
        # тестовая модель
        category = ProductCategory.objects.create(name='category 1')
        Product.objects.create(category=category, name='product 1')
        Product.objects.create(category=category, name='product 2')
        # для обращений к html страницам
        self.client = Client()

    def test_mainapp_urls(self):
        '''Код тестирующий URL главную, контакты, продукты'''

        # проверка результата
        # self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

    def test_mainapp_product_urls(self):
        '''URL продуктов и категорий'''

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        # for category in ProductCategory.objects.filter(is_active=True):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

        # response = self.client.get('/products/category/0/')
        # self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)

    # # tearDown - выполняется после setUp. tearDown - можно пока опустить
    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', \
    #                  'basketapp')
