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
    User_order.objects.create(
        user = User.objects.get(username='user1234'),
        adress = '인천광역시 연수구 114-14',
        receive_name = '김초록',
        receive_phone = '010-2222-3333',
        orderstatus = 1,
        received_date = datetime.datetime.now()

    )