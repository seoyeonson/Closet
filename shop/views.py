from unicodedata import category
from django.shortcuts import render, redirect

from shop.models import Product

from django.shortcuts import render, HttpResponse
from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
def main(request):
    main_cg = 3
    products = Product.objects.filter(category_code_id=main_cg).values('product_name', 'product_price').distinct()
    category = Product_category.objects.filter(category_code=main_cg).values('category_name')
    
    # for product in products:
    #     print(product)

    context = {
        'category': category[0],
        'products' : products,
    }
    return render(request, 'index.html', context)

def list(request, cg):
    products = Product.objects.filter(category_code_id=cg).values('product_name', 'product_price').distinct()
    category = Product_category.objects.filter(category_code=cg).values('category_name')

    context = {
        'products' : products,
        'category' : category[0]
    }
    return render(request, 'index.html', context)

def product(request, name):
    product = Product.objects.filter(product_name=name).values('product_name', 'product_price', 'product_rate', 'product_num').distinct()
    product_colors = Product.objects.filter(product_name=name).values('product_color')
    product_sizes = Product.objects.filter(product_name=name).values('product_size')

    # print(product[0].get('product_name'))
    for products in product_colors:
        print(products)

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

def test_images(requests, pk):
    product = Product.objects.filter(pk=pk)
    print(type(product))
    return HttpResponse(f'''
        <h2>Images<h2>
        ''')