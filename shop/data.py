from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
import datetime
import random
import re
from config.ProductName import ProductName


# 의도 --> 서비스 연결
def service(username, intent_name, query, ner_tags=None):
    
    product = Recommend_product(ProductName.name).product
    user_info = User_info(username)
    order = Order(username)
    result = None

    print(type(ner_tags))

    if intent_name == '주문수량확인':
        try:
            user_info.cart_insert(product[0], query)
            return None
        except Exception as ex:
            print(ex)
            return None

    elif ((intent_name == '상품추천요청') and (ner_tags != None)) or (intent_name == '카테고리선택'):
        try:
            result = product[:1].values()[0] # 상품의 모든 정보가 담긴 쿼리셋
            result['product_date'] = str(result['product_date'])
        except Exception as ex:
            print(ex)
        return result

    elif intent_name == '상품색상문의':
        try: 
            result = list(product.values('product_color')) # 컬러 정보가 담긴 쿼리셋
            print(result)
            if result[0]['product_color'] == '':
                return '색상 정보가 없습니다'
            result = [i['product_color'] for i in result]
            result = '<br>'.join(result)        
        except Exception as ex:
            print(ex)
            result = None
        return result # 컬러 정보가 담긴 쿼리셋

    elif intent_name == '상품가격문의':
        try: 
            result = '<br><br>' + str(product[:1].values('product_price')[0].get('product_price'))
        except Exception as ex:
            print(ex)
            result = None
        return result

    elif intent_name == '상품사이즈문의':
        try:
            result = list(product.values('product_size')) # 컬러 정보가 담긴 쿼리셋
            if result[0]['product_size'] == '':
                return '사이즈 정보가 없습니다'
            result = [i['product_size'] for i in result]
            result = '<br>'.join(result)
        except Exception as ex:
            print(ex)
            result = None
        return result

    elif (intent_name == '반품요청') or (intent_name == '주문취소요청') :
        try:
            result = order.order_info()
        except Exception as ex:
            print(ex)
            result = None 
        return result
    
    # elif intent_name == '주문취소요청':
    #     return order.order_info()

    # elif intent_name == '':
    #     return order.order_info()
    
    else:
        return None


# 상품 (Product) 정보 조회

class Recommend_product():
    
    def __init__(self, product_name):
        self.product = Product.objects.filter(product_name = product_name)

    def __str__(self):
        return self.product


# 주문 관련

class Order():

    def __init__(self, username):
        self.user = User.objects.get(username=username)

        try:
            self.order = User_order.objects.filter(user=self.user).order_by('-order_num')[:1].values()[0]
        except :
            self.order = False

    # 주문내역 조회
    def order_info(self):
        order = self.order

        if not(order):
            data = '주문정보없음'
        else:
            order_detail = User_order_detail.objects.get(order_num=order.get('order_num'))

            received_date = f'수령일: {order.get("received_date")}' if order.get('received_date') != None else ''

            data = f'''<br><br>주문번호: {order.get('order_num')}<br> 
                        주문상품: {order_detail.product_num.product_name}<br> 
                        주문수량: {order_detail.product_count}<br> 
                        주문금액: {order_detail.product_price}<br> 
                        주문일시: {order.get('order_date')}<br> 
                        주소: {order.get('adress')}<br> 
                        수령인: {order.get('receive_name')}<br> 
                        전화번호: {order.get('receive_phone')}<br> 
                        주문상태: {User_order.ORDERSTATUS[order.get('orderstatus')-1][1]}<br> ''' + received_date

        
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
    def cart_insert(self, product, query):
        product_count = int(re.sub('[^0-9]', ' ', query).split(' ')[0]) # ex) '100개' 입력시 100만 가져오기 
        Cart.objects.create(
            product_num = product,
            u_id= self.user,
            product_count=product_count
        )
        return '장바구니 등록 완료'