from django.shortcuts import redirect, render
from django.db.models import Prefetch
from requests import request
from orders.models import Order, OrderItem
from carts.models import Cart
from .forms import UserLoginForm, UserRegistrationForm, UserChangeForm
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def login(request):

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key
            if user:
                auth.login(request, user)
                messages.success(request, "You are successfully logged in!")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                if redirect_page:
                    return HttpResponseRedirect(request.POST.get("next"))
                return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserLoginForm()
    context = {
        "form": form,
        "title": "Login",
    }
    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key
            user = form.instance
            # auth.login(request, user)


            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, "You are successfully registered!")
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "form": form,
        "title": "Registration",
    }
    return render(request, "users/registration.html", context)

@login_required
def profile(request):
    if request.method == "POST":
        form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile is successfully updated!")
            return HttpResponseRedirect(reverse("users:profile"))
        
    else:
        form = UserChangeForm(instance=request.user)

    

    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")    
    
    context = {
        "form": form,
        "title": "Profile",
        "orders": orders
    }
    return render(request, "users/profile.html", context)

@login_required
def logout(request):
    messages.success(request, "You are successfully logged out!")
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))



def users_cart(request):
    return render(request, "users/users_cart.html")








