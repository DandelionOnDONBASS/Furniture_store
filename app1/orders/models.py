from django.db import models

from goods.models import Products
from users.models import User

# Create your models here.
class OrderItemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self) 
        return 0


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT,blank=True,null=True, default=None, verbose_name="Пользователь")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(default=False ,verbose_name="Требуется доставка")
    delivery_address = models.TextField(null=True, blank=True ,verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False ,verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False ,verbose_name="Оплачено")
    status = models.CharField(max_length=50, default= "В обработке", verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        
    def __str__(self):
        return f'Заказ №{self.pk} | {self.user.first_name} {self.user.last_name}'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Products, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Товар", default=None)
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая стоимость", blank=True, null=True)

    
    class Meta:
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderItemQueryset.as_manager()
    
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
    def product_price(self):
        return round(self.price * self.quantity, 2)
        
    def __str__(self):
        return f'{self.product.name} | {self.order.user.first_name} {self.order.user.last_name}'
    
    

    