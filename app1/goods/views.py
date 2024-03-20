from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from goods.models import Products
from goods.utils import q_search
from users.models import Comment


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    
    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    comments = Comment.objects.filter(product=product).order_by('-created')
    context = {"product": product,
               "comments": comments}

    return render(request, "goods/product.html", context=context)


@login_required
def comment(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    Comment.objects.create(author=request.user, product=product, text=request.POST.get('comment-text'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

    
