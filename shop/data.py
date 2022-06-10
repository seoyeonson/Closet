from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
import datetime
import random

# 상품 (Product) 정보 조회

class Recommend_product():
    
    def __init__(self, product_num):
        self.product = Product.objects.get(product_num = product_num)

    def __str__(self):
        return self.product


# 주문 관련

class Order():

    def __init__(self, username):
        self.user = User.objects.get(username=username)  
        self.order = User_order.objects.filter(user=self.user).order_by('-order_num')[:1].values()[0]


    # 주문내역 조회

    def order_info(self):
        # try:
        order = self.order
        order_detail = User_order_detail.objects.get(order_num=order.get('order_num'))

        received_date = f'수령일: {order.get("received_date")}' if order.get('received_date') != None else ''
        data = f'''주문번호: {order.get('order_num')}\n 주문상품: {order_detail.product_num.product_name}\n주문수량: {order_detail.product_count}\n 주문금액: {order_detail.product_price}\n
        주문일시: {order.get('order_date')}\n주소: {order.get('adress')}\n수령인: {order.get('receive_name')}\n전화번호: {order.get('receive_phone')}\n
        주문상태: {User_order.ORDERSTATUS[order.get('orderstatus')-1][1]}\n''' + received_date
        # except:
        #     data = '주문정보없음'
        
        return data

    # 주문 상태 조회
    def order_status(self):
        order = self.order
        return User_order.ORDERSTATUS[order.get('orderstatus')-1][1]

    # 주문 취소 (주문 삭제)
    def order_delete(self):
        order = self.order
        order_detail = User_order_detail.objects.get(order_num=order.get('order_num'))
        User_order.objects.get(order_num=order.get('order_num')).delete()
        order_detail.delete()


    # 반품 처리 (주문상태 변경)

    def order_update(self, num):
        order = self.order
        order = User_order.objects.get(order_num=order.get('order_num'))
        if num == 0: # 주문취소 하는 경우
            order.order_status = 6
        elif num == 1: # 반품신청 하는 경우
            order.order_status = 7
        order.save()
        return '반품 처리 완료'


# 유저 쿠폰조회 / 장바구니 상품등록
class User_info():

    def __init__(self, username):
        self.user = User.objects.get(username=username) 
    
    # 유저 보유한 쿠폰 조회
    def cuppon_search(self):
        cuppon = Cuppon.objects.get(u_id=self.user.u_id)
        return cuppon

    # 장바구니에 상품 등록 (주문접수)
    def cart_insert(self, product_num, product_count):
        product = Product.objects.get(product_num=product_num)
        Cart.objects.create(
            product_num = product,
            u_id= self.user,
            product_count=product_count
        )
        return '장바구니 등록 완료'