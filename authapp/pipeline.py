import datetime
import os
from collections import OrderedDict
from urllib.parse import urlunparse, urlencode

import requests
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from geekshop import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # api_url = "https://api.vk.com/method/users.get?fields=bdate,sex,about"
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max_orig')),
                                                access_token=response['access_token'], v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)

    # если не успешно "!= 200"
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    # print('resp.json()', resp.json()['response'][0])
    # пол
    if data['sex']:
        # user.shopuserprofile.gender = ShopUserProfile.MALE
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        if data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        # else:
        #     ShopUserProfile.FEMALE
    # о себе
    if data['about']:
        user.shopuserprofile.about_me = data['about']
    # заполнено ли у пользователя поле дата рождения
    try:
        if data['bdate']:
            bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            # age = timezone.now().date().year - bdate.year
            age = datetime.datetime.now().date().year - bdate.year
            if age < 18:
                user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    except KeyError:
        data['bdate'] = None

    if data['last_name']:
        user.username = data['last_name']

    # print('photo_max_orig', data['photo_max_orig'])
    # print('api_url', api_url)
    if data['photo_max_orig']:
        # url = data['photo_max_orig']
        photo = requests.get(data['photo_max_orig'])
        if photo.status_code == 200:
            # photo = url.split("/")[-1]
            # photo = url.content
            # photo_name = f'users_avatars/{user.id}.jpg' - при "user.username" подхватывается id из vk
            photo_name = f'users_avatars/{user.id}.jpg'
            # with open(os.path.join(settings.BASE_DIR, f'media/{photo_name}'), "wb") as avatar:
            with open(f'media/{photo_name}', "wb") as avatar:
                # avatar.write(photo.content)
                avatar.write(photo.content)
                user.avatar = photo_name
            # print('photo_name', photo_name)
            # print('ShopUserProfile.user.name', user.id)
    user.save()
