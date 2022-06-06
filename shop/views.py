from django.shortcuts import render
from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
def main(request):
    return render(request, 'index.html')

def product(request, pk):
    return render(request, 'product.html')

def mypage(request):
    return render(request, 'mypage.html')

def cart(request):
    return render(request, 'cart.html')

def test_images(request, id):
    product = Product.objects.get(pk=id)
    # count = product.count()
    # user = User.objects.filter(u_id=id)
    context = {
        'product': product,
    }
    return render(request, 'test_images.html', context)

