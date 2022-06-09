from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
import datetime
import random

def User_Insert():
    # 유저정보 생성하는 함수입니다. 가상의 유저 300명 생성합니다.
    for i in range(300):
        User.objects.create(
            username = f'user{i}',
            password = 'password',
            name = '홍길동',
            nickname = f'nickname{str(i)}',
            email = f'user{str(i)}@test.com',
            sociallogin = f'user{str(i)}@test.com',
            mobile = '010-2222-0' + str(i+100),
            receive_marketing = True if i % 2 == 0 else False )

def Grade_Insert():
    for i in range(1, 301): # 300명의 전체 유저가, 10개의 각각다른 상품(랜덤)에 대해 평점(랜덤)을 매깁니다. 
        for j in range(10):
            Grade.objects.create(
                u_id = User.objects.get(u_id=i),
                product_num = Product.objects.get(product_num=random.randint(1, 8315)),
                grade = random.randint(0, 5)
            )


def User_order_Insert():
    # 유저의 주문정보 데이터를 입력하는 함수입니다. 함수 실행할때마다 1개의 주문이 입력됩니다.

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
    # 실행시마다 데이터 1개씩 생성됩니다. 
    product = Product.objects.get(product_num=5)
    user = User.objects.get(username='user1234')
    Cart.objects.create(
        u_id = user,
        product_num = product,
        product_count = 3
    )

def Cuppon_Insert():
    # 실행시마다 데이터 1개씩 생성됩니다.
    Cuppon.objects.create(
        discount_rate = 0.1,
        cuppon_num = 1,
        u_id = User.objects.get(username='user1234')
    )
