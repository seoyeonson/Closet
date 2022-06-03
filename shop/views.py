from unicodedata import category
from django.shortcuts import render

from shop.models import Product

from django.shortcuts import render, HttpResponse
from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
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

def test_images(requests, pk):
    product = Product.objects.filter(pk=pk)
    print(type(product))
    return HttpResponse(f'''
        <h2>Images<h2>
        ''')