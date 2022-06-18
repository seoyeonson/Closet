from pyparsing import col
from config.now_state import now_state
from shop.models import Product, Product_category, User, User_order, User_order_detail, Cart, Cuppon, Customer_inquiry, Grade
import datetime
import random
import re
from config.ProductName import ProductName


# 의도 --> 서비스 연결
def service(username, state, info):
    if ProductName.name:
        product_class = Recommend_product(ProductName.name)
        product = product_class.product
    order = Order(username)
    result = None
    order_product_info = info


    # if intent_name == '주문수량확인':
    #     try:
    #         user_info.cart_insert(product[0], query)
    #         return None
    #     except Exception as ex:
    #         print(ex)
    #         return None

    # 상품추천요청 (카테고리 개체명 있는 경우)
    if state == 1:
        try:
            result = product[:1].values()[0] # 상품의 모든 정보가 담긴 쿼리셋
            result['product_date'] = str(result['product_date'])
        except Exception as ex:
            print(ex)
        return result

    # 색상문의
    elif state == 5:
        try: 
            now_state.state = 1
            colors = product_class.color_info()
            if colors == []:
                return '색상 정보가 없습니다'                
            result = '<br><br>' + '<br>'.join(colors)        
        except Exception as ex:
            print(ex)
            result = None
        return result # 컬러 정보가 담긴 쿼리셋

    # 가격문의
    elif state == 3:
        try: 
            now_state.state = 1
            result = '<br><br>' + str(product[:1].values('product_price')[0].get('product_price')) + '원'
        except Exception as ex:
            print(ex)
            result = None
        return result

    # 사이즈 문의
    elif state == 4:
        try:
            now_state.state = 1
            sizes = product_class.size_info()
            if sizes == []:
                return '사이즈 정보가 없습니다'
            result = '<br><br>' + '<br>'.join(sizes)
        except Exception as ex:
            print(ex)
            result = None
        return result

    # 주문정보 확인 (반품 or 주문취소)
    elif (state == 8) or (state == 9):
        try:
            result = order.order_info()
        except Exception as ex:
            print(ex)
            result = None 
        return result

    elif state == 11: # 반품신청
        order.order_update(1)
        now_state.state = 0
        return '반품신청 완료되었습니다.<br>반품진행 내역은 마이페이지에서 확인 가능합니다.<br><br><a href="http://127.0.0.1:8000/mypage/" target="_blank" class="go_product">확인하러 가기</a>'

    elif state == 12: # 주문취소
        order.order_update(0)
        now_state.state = 0
        return '주문취소 완료되었습니다.<br>주문취소 내역은 마이페이지에서 확인 가능합니다.<br><br><a href="http://127.0.0.1:8000/mypage/" target="_blank" class="go_product">확인하러 가기</a>'

    # 주문옵션 선택
    elif state == 6:
        result = {
            'notice': '옵션입력',
            'sizes': product_class.size_info(),
            'colors': product_class.color_info(),
        }
        return result

    elif state == 7: # FSM 완료 후 state 값 정해지면 변경
        try:
            order = order.order_insert(ProductName.name, order_product_info)
            now_state.state = 0
            return None
        except Exception as ex:
            print(ex)
            return None

    # elif state == '주문취소요청 -> 긍정':
    #   return order.order_delete()
          
    # elif state == '반품요청 -> 긍정':
    #   return order.order_update()
    
    elif state == 10:
        try:
            user_info = User_info(username)
            result = user_info.cuppon_search()
            return result
        except Exception as ex:
            print(ex)
    else:
        return None


# 상품 (Product) 정보 조회

class Recommend_product():
    
    def __init__(self, product_name):
        self.product = Product.objects.filter(product_name = product_name)

    def __str__(self):
        return self.product
    
    def color_info(self):
        result = list(self.product.values('product_color')) # 컬러 정보가 담긴 쿼리셋
        result = [i['product_color'] for i in result]
        if result[0]== '':
            return []
        return result
    
    def size_info(self):
        result = result = list(self.product.values('product_size')) # 사이즈 정보가 담긴 쿼리셋
        result = [i['product_size'] for i in result]
        if result[0] == '':
            return []
        return result

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

            received_date = f'- 수령일: {order.get("received_date").strftime("%Y/%m/%d")}<br>' if order.get('received_date') != None else ''
            # received_date = f'<p>수령일: {order.get("received_date")}</p>' if order.get('received_date') != None else ''

            data = f'''<br><br>- 주문번호: {order.get('order_num')}<br> 
                        - 주문상품: {order_detail.product_num.product_name}<br> 
                        - 주문수량: {order_detail.product_count}<br> 
                        - 주문금액: {order_detail.product_price}<br> 
                        - 주문일시: {order.get('order_date').strftime('%Y/%m/%d %H:%M:%S')}<br> 
                        - 주소: {order.get('adress')}<br> 
                        - 수령인: {order.get('receive_name')}<br> 
                        - 전화번호: {order.get('receive_phone')}<br> 
                        - 주문상태: {User_order.ORDERSTATUS[order.get('orderstatus')-1][1]}<br> ''' + received_date

            # data = f'''<div>
            #             <div><p style="width: 50%">{order_detail.product_num.product_name}</p> <img src="/media/{order_detail.product_num.product_image}" style="width: 50%"></div>
            #             <hr>
            #             <p>주문번호: {order.get('order_num')}</p>
            #             <p>주문일시: {order.get('order_date')}</p>
            #             <p>주문수량: {order_detail.product_count}</p>
            #             <p>주소: {order.get('adress')}</p>
            #             <p>수령인: {order.get('receive_name')}</p>
            #             <p>전화번호: {order.get('receive_phone')}</p>
            #             <p>주문상태: {User_order.ORDERSTATUS[order.get('orderstatus')-1][1]}</p>'''+ received_date + '</div>'


        
        return data

    # 주문 상태 조회
    def order_status(self):
        order = self.order
        return User_order.ORDERSTATUS[order.get('orderstatus')-1][1]

    def order_insert(self, product_name, order_product_info):
        # 유저의 주문정보 데이터를 입력하는 함수입니다. 함수 실행할때마다 1개의 주문이 입력됩니다.
        try:
            User_order.objects.create(
                user = self.user,
                adress = '강남구 테헤란로 100',
                receive_name = self.user.name,
                receive_phone = self.user.mobile,
                orderstatus = 1,
                received_date = datetime.datetime.now()
            )
            order = User_order.objects.filter(user=self.user.u_id).order_by('-received_date')[0]
            color = order_product_info['color']
            size = order_product_info['size']
            # print(color, size, order_product_info['product_count'], type(order_product_info['product_count']))
            product = Product.objects.filter(product_name=product_name, product_color=color, product_size=size).first()
            product_count = int(order_product_info['product_count'])

            User_order_detail.objects.create(
                product_num = product,
                order_num = order,
                product_count = product_count,
                product_price = product.product_price * product_count
            )
        except Exception as ex:
            print('주문등록실패')
            print(ex)

    # 주문 취소 (주문 삭제)
    def order_delete(self):
        order = self.order
        order_detail = User_order_detail.objects.get(order_num=order.get('order_num'))
        User_order.objects.get(order_num=order.get('order_num')).delete()
        order_detail.delete()


    # 반품 처리 (주문상태 변경)

    def order_update(self, num):
        try:
            order = self.order
            print('filter : ',order)
            order = User_order.objects.get(order_num=order.get('order_num'))
            print(order.orderstatus)
            if num == 0: # 주문취소 하는 경우
                order.orderstatus = 6
            elif num == 1: # 반품신청 하는 경우
                order.orderstatus = 7
            order.save()
        except Exception as ex:
            print('order_update 실패')
            print(ex)
        return num


# 유저 쿠폰조회 / 장바구니 상품등록
class User_info():

    def __init__(self, username):
        self.user = User.objects.get(username=username)
    
    # 유저 보유한 쿠폰 조회
    def cuppon_search(self):
        try:
            cuppon = Cuppon.objects.get(u_id=self.user.u_id)
            percentage = int(cuppon.discount_rate * 100)
            result = f'<br><{percentage}% 할인 쿠폰<br>수량: {cuppon.cuppon_num}개>'
            print('쿠폰: ', percentage, cuppon)

        except Exception as ex:
            print('쿠폰 함수')
            print(ex)
        return result

    

    # # 장바구니에 상품 등록 (주문접수)
    # def cart_insert(self, product, query):
    #     product_count = int(re.sub('[^0-9]', ' ', query).split(' ')[0]) # ex) '100개' 입력시 100만 가져오기 
    #     Cart.objects.create(
    #         product_num = product,
    #         u_id= self.user,
    #         product_count=product_count
    #     )
    #     return '장바구니 등록 완료'