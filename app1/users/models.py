from django.db import models
from django.contrib.auth.models import AbstractUser
from goods.models import Products


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Пользоватля'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text