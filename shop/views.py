from unicodedata import category
from django.shortcuts import render, redirect

from shop.models import Product

from django.shortcuts import render, HttpResponse
from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
def main(request):
    main_cg = 3
    products = Product.objects.filter(category_code_id=main_cg).values('product_name', 'product_price', 'product_image').distinct()
    category = Product_category.objects.filter(category_code=main_cg).values('category_name')
    
    for product in products:
        print(product)

    context = {
        'category': category[0],
        'products' : products,
    }
    return render(request, 'index.html', context)

def list(request, cg):
    products = Product.objects.filter(category_code_id=cg).values('product_name', 'product_price', 'product_image').distinct()
    category = Product_category.objects.filter(category_code=cg).values('category_name')

    context = {
        'products' : products,
        'category' : category[0]
    }
    return render(request, 'index.html', context)

def product(request, name):
    product = Product.objects.filter(product_name=name).values('product_name', 'product_price', 'product_rate', 'product_num', 'product_image').distinct()
    product_colors = Product.objects.filter(product_name=name).values('product_color')
    product_sizes = Product.objects.filter(product_name=name).values('product_size')

    colors_cnt = 0
    size_cnt = 0
    for products in product_colors:
        if products.get('product_color') != '':
            colors_cnt += 1

    for products in product_sizes:
        if products.get('product_size') != '':
            size_cnt += 1

    if colors_cnt == 0:
        product_colors = {}

    if size_cnt == 0:
        product_sizes = {}
    
    print(product_colors)
    print(product_sizes)

    if request.method=="GET":
        context = {
            'product' : product[0],
            'product_colors' : product_colors,
            'product_sizes' : product_sizes,
        }
        return render(request, 'product.html', context)

    elif request.method=="POST":

        print(product[0].get('product_num'))

        # cart = Cart(
        #     product_num = product[0].get('product_num'),
        #     u_id = 0,
        #     product_count = 1,    
        # )

        # cart.save()

        return redirect(f'/cart/')

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

