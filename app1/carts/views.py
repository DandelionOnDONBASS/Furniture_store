from django.shortcuts import redirect, render
from .utils import get_user_cart
from goods.models import Products
from .models import Cart
from django.http import JsonResponse
from django.template.loader import render_to_string

def cart_add(request):
    
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)
    user_cart = get_user_cart(request)
    cart_item_html = render_to_string('includes/included_cart.html', {'carts': user_cart}, request=request)
    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_item_html
    }

    return JsonResponse(response_data)


def cart_change(request):

    cart_id = request.POST.get('cart_id')
    quantity = request.POST.get('quantity')
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()

    updated_quantity = cart.quantity

    cart = get_user_cart(request).order_by('created_timestamp')
    cart_items_html = render_to_string('includes/included_cart.html', {'carts': cart}, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quantity": quantity
    }

    return JsonResponse(response_data)
    

def cart_remove(request):

    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_cart(request).order_by('created_timestamp')
   
    cart_items_html = render_to_string('includes/included_cart.html', {'carts': user_cart}, request=request)

    print(user_cart)
    response_data = {
        "message": "Товар удален из корзины",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity        
    }

    return JsonResponse(response_data)