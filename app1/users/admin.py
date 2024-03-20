from django.contrib import admin
from .models import User, Comment
from orders.admin import OrderInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    inlines = [OrderInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'text', 'created']


