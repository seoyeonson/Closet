from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
import datetime

def User_Insert():
    User.objects.create(
        username = 'user1234',
        password = 'user1234',
        name = '김초록',
        nickname = '초록',
        email = 'green@test.com',
        sociallogin = 'green@test.com',
        receive_marketing = True)



def User_order_Insert():
    # user = User.objects.get(username='user1234'),

    User_order.objects.create(
        user = User.objects.get(username='user1234'),
        adress = '인천광역시 연수구 114-14',
        receive_name = '김초록',
        receive_phone = '010-2222-3333',
        orderstatus = 1,
        received_date = datetime.datetime.now()
    )
    order = User_order.objects.order_by('-user')[0]
    product = Product.objects.get(product_num=1)
    product_count = 5

    User_order_detail.objects.create(
        product_num = product,
        order_num = order,
        product_count = product_count,
        product_price = product.product_price * product_count
    )


def Cart_Insert():
    product = Product.objects.get(product_num=5)
    user = User.objects.get(username='user1234')
    Cart.objects.create(
        u_id = user,
        product_num = product,
        product_count = 3
    )

def Cuppon_Insert():
    Cuppon.objects.create(
        discount_rate = 0.1,
        cuppon_num = 1,
        u_id = User.objects.get(username='user1234')
    )
