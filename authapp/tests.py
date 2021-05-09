from django.conf import settings
from django.test import TestCase
from django.test.client import Client


# Create your tests here.
from authapp.models import ShopUser


class UserAuthTestCase(TestCase):
    # код успеха
    SUCCESS_STATUS_CODE = 200
    # редирект, перенаправление
    REDIRECT_STATUS_CODE = 302

    REDIRECT_STATUS_CODE_2 = 301
    # запрещённый
    FORBIDDEN_STATUS_CODE = 403

    def setUp(self):
        self.client = Client()
        # users
        self.superuser = ShopUser.objects.create_superuser('django', 'django2@gb.local', 'geekbrains')

        self.user = ShopUser.objects.create_user('django2', 'django2@gb.local', 'geekbrains')

        # self.user_with__first_name = ShopUser.objects.create_user('umaturman', \
        #                                                           'umaturman@gb.local', 'geekbrains',
        #                                                           first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertContains(response, 'Войти')
        self.assertEqual(response.context['title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=self.SUCCESS_STATUS_CODE)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='django2', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)
        self.assertNotContains(response, 'Войти', status_code=self.SUCCESS_STATUS_CODE)
        self.assertContains(response, 'Пользователь', status_code=self.SUCCESS_STATUS_CODE)
        self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    def test_user_register(self):
        '''Регистрация пользователя'''
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)
        # self.assertEqual(response.context['title'], 'регистрация')
        # self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'django4',
            'first_name': 'django4',
            'last_name': 'django4',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'django4@gb.local',
            'age': '33'
        }

        # запрос            метод POST  адрес           данные формы
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)
        # проверка созданного пользователя
        new_user = ShopUser.objects.get(username=new_user_data['username'])
        self.assertFalse(new_user.is_active)

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"
        # переходим по этому адресу
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

        # обновляем пользователя из базы
        new_user.refresh_from_db()

        # проверяем, что он теперь активирован
        self.assertTrue(new_user.is_active)


    #     # данные нового пользователя
    #     self.client.login(username=new_user_data['username'], \
    #                       password=new_user_data['password1'])
    #
    #     # логинимся
    #     response = self.client.get('/auth/login/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(response.context['user'].is_anonymous)
    #
    #     # проверяем главную страницу
    #     response = self.client.get('/')
    #     self.assertContains(response, text=new_user_data['first_name'], \
    #                         status_code=200)
    #
    # def test_user_wrong_register(self):
    #     new_user_data = {
    #         'username': 'teen',
    #         'first_name': 'Мэри',
    #         'last_name': 'Поппинс',
    #         'password1': 'geekbrains',
    #         'password2': 'geekbrains',
    #         'email': 'merypoppins@geekshop.local',
    #         'age': '17'}
    #
    #     response = self.client.post('/auth/register/', data=new_user_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'register_form', 'age', \
    #                          'Вы слишком молоды!')

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, self.REDIRECT_STATUS_CODE)

        # с логином все должно быть хорошо
        self.client.login(username='django2', password='geekbrains')

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)
        # не верно "<QuerySet []> != []":
        # self.assertEqual(response.context['basket'], [])
        # верно:
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        # self.assertEqual(response.request['PATH_INFO'], '/basket/')
        # self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def test_products_category(self):
        '''Тест активной категории'''
        response = self.client.get('/products/category/1/')
        self.assertEqual(response.status_code, self.SUCCESS_STATUS_CODE)


