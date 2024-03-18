from django.contrib import admin
from .models import Order, OrderItem

class OrderInline(admin.TabularInline):
    model = Order
    fields = ('created_timestamp','requires_delivery', 'delivery_address', 'phone_number')
    readonly_fields = ('created_timestamp',)
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'name', 'price', 'quantity','total_price')
    extra = 0
    readonly_fields = ('total_price','quantity','price')
 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_timestamp', 'payment_on_get', 'is_paid', 'status')
    list_filter = ('user', 'created_timestamp', 'payment_on_get', 'is_paid', 'status')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'name', 'price', 'quantity', 'created_timestamp')
    list_filter = ('order', 'product', 'name', 'price', 'quantity', 'created_timestamp')
