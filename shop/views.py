from unicodedata import category
from django.shortcuts import render

from shop.models import Product

def main(request):
    products = Product.objects.filter(category_code_id=3)

    context = {
        products : products,
    }
    return render(request, 'index.html', context)

def product(request, pk):
    return render(request, 'product.html')

def mypage(request):
    return render(request, 'mypage.html')

def cart(request):
    return render(request, 'cart.html')