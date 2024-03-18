from django.contrib import admin
from .models import User
from orders.admin import OrderInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    inlines = [OrderInline]
# Register your models here.
