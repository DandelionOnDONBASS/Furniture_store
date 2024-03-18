from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Пользоватля'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username