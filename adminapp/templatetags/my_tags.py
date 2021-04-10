from django import template
from django.conf import settings

register = template.Library()

# 1-й вариант с декоратором
@register.filter(name='media_folder_users')
def media_folder_users(path_to_avatar):
    # def media_for_users(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам пользователей
    users_avatars/user1.jpg --> /media/users_avatars/user1.jpg
    """
    if not path_to_avatar:
        path_to_avatar = 'users_avatars/default.jpg'
    return f'{settings.MEDIA_URL}{path_to_avatar}'

# 2-й вариант, без декоратора, но с регистрацией
def media_folder_products(path_to_image):
    # def media_for_products(string):
    """Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg"""

    if not path_to_image:
<<<<<<< HEAD
        path_to_image = 'products_images/default.png'
=======
        path_to_image = 'products_images/default.jpg'
>>>>>>> lesson_9

    return f'{settings.MEDIA_URL}{path_to_image}'


register.filter('media_folder_products', media_folder_products)
