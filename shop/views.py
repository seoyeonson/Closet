from unicodedata import category
from django.shortcuts import render, redirect

from shop.models import Product

from django.shortcuts import render, HttpResponse
from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
def main(request):
    main_cg = 3
    products = Product.objects.filter(category_code_id=main_cg).values('product_name', 'product_price', 'product_image').distinct()
    category = Product_category.objects.filter(category_code=main_cg).values('category_name')
    
    # for product in products:
    #     print(product)

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
    isColor = True
    isSize = True

    for products in product_colors:
        if products.get('product_color') != '':
            colors_cnt += 1

    for products in product_sizes:
        if products.get('product_size') != '':
            size_cnt += 1

    if colors_cnt == 0:
        isColor = False

    if size_cnt == 0:
        isSize = False

    if request.method=="GET":
        context = {
            'product' : product[0],
            'isColor' : isColor,
            'isSize' : isSize,
            'product_colors' : product_colors,
            'product_sizes' : product_sizes,
        }
        return render(request, 'product.html', context)

    elif request.method=="POST":

        # print(product[0].get('product_num'))

        # cart = Cart(
        #     product_num = product[0].get('product_num'),
        #     u_id = 0,
        #     product_count = 1,    
        # )

        # cart.save()

        return redirect(f'/cart/')

def mypage(request):
    user = User.objects.get(u_id=1)
    orders = User_order_detail.objects.filter(user=user)
    all_orders = len(orders)

    cuppons = Cuppon.objects.all()
    all_cuppons = len(cuppons)

    context = {
        'user': user,
        'orders': orders,
        'all_orders': all_orders,
        'cuppons': cuppons,
        'all_cuppons': all_cuppons,
    }

    return render(request, 'mypage.html', context)

def cart(request):
    user = User.objects.get(u_id=1)
    carts = Cart.objects.filter(user=user)
    all_prods = len(carts)

    all_price = 0
    for cart in carts:
       all_price += cart.product_num.product_price * cart.product_count 

    # carts.product_num.

    context = {
        'carts' : carts,
        'all_prods' : all_prods,
        'all_price' : all_price,
    }
    return render(request, 'cart.html', context)

def test_images(request, id):
    product = Product.objects.get(pk=id)
    order = User_order.objects.get(pk=1)
    # count = product.count()
    # user = User.objects.filter(u_id=id)
    context = {
        'product': product,
        'order': order,
    }
    return render(request, 'test_images.html', context)

