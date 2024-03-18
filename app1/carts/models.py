from django.db import models
from users.models import User
from goods.models import Products



class CartQuaryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(Products, on_delete=models.CASCADE,verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество",default=0)
    session_key = models.CharField(max_length=128, blank=True, null=True, verbose_name="Ключ сессии")
    created_timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    objects = CartQuaryset().as_manager()

    def __str__(self):
        if self.user:
            return 'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
        
        return 'Аннимный юзер | Товар {self.product.name} | Количество {self.quantity}'
    

    def products_price(self):
        return round(self.product.sell_price() * self.quantity ,2)