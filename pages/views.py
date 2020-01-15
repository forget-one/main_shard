from django.shortcuts import render, get_object_or_404, redirect
from mixture.models import *
from django.core.paginator import Paginator
from pages.context_proccesor import *
# Create your views here.

def home(request):
    products    = Product.objects.all()  
    paginator   = Paginator(products, 4) 
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)
    is_paginated= page_obj.has_other_pages()
    if page_obj.has_previous():
        prev_url    = f'?page={page_obj.previous_page_number()}'
    else:
        prev_url    = ''
    if page_obj.has_next():
        next_url    = f'?page={page_obj.next_page_number()}'
    else:
        next_url    = ''
    return render(request, 'pages/home.html', locals())


def category(request, slug):
    category    = get_object_or_404(Category, slug=slug)
    category_qs = Product.objects.filter(category=category)
    return render(
        request,
        'pages/category.html',
        {
        'category': category_qs
        }
    )


def product(request, slug):
    product     = Product.objects.get(slug=slug)
    return render(request, 'pages/product.html', locals()) 


def checkout(request):
    return render(request, 'pages/checkout.html')

def summary(request):
    cart_items  = CartItem.objects.filter(
    cart        = get_cart(request),
    ordered     = False)
    total_price = get_total_price(request)

    return render(request, 'pages/summary.html', locals())    


def add_cart(request, slug):
    cart        = get_cart(request)
    product     = Product.objects.get(slug=slug)
    cart_item, created = CartItem.objects.get_or_create(
        cart        = cart,
        product     = product,
        ordered     = False,
    )
    if  request.POST.get('count'):
        cart_item.count = abs(int(request.POST.get('count')))
        cart_item.save()
    else:
        cart_item.count = 1
    return redirect('summary')

def remove_from_cart(request, slug):
    cart        = get_cart(request)
    product     = Product.objects.get(slug=slug)
    cart_item   = CartItem.objects.get(
        cart        = cart,
        product     = product,
        ordered     = False).delete()
    return redirect('product', slug=slug)


def cart_item_single_plus(request, slug):
    cart        = get_cart(request)
    product     = Product.objects.get(slug=slug)
    cart_item   = CartItem.objects.get(
        cart        = cart,
        product     = product,
        ordered     = False)
    cart_item.count += 1
    cart_item.save()
    return redirect('summary')


def cart_item_single_minus(request, slug):
    cart        = get_cart(request)
    product     = Product.objects.get(slug=slug)
    cart_item   = CartItem.objects.get(
        cart        = cart,
        product     = product,
        ordered     = False)
    if cart_item.count > 1:
        cart_item.count -= 1
    cart_item.save()
    return redirect('summary')