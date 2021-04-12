from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст', default=18)

    # send message
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expired(self):
        now_date = now() - timedelta(hours=48)
        if now_date <= self.activation_key_expires:
            return False
        return True

class ShopUserProfile(models.Model):
    # choices - вариант выбора заданный жёстко
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = {
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    }

    # Связь один к одному, уникальный, не нулевой "False",
    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tag_line = models.CharField(verbose_name='теги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    # сигнал(post_save) - действие с оъектом
    # sender - кто прислал нам сигнал, instance - объект, created
    # сигнал на создание
    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    # сигнал на обновление
    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()