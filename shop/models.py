from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True) # 아이디
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)     # 본명
    nickname = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=128, )
    address = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=16, unique=True)
    gender = models.CharField(max_length=2, null=True)
    age = models.CharField(max_length=8, null=True)
    sociallogin = models.CharField(max_length=16)
    date_joined = models.DateField(auto_now_add=True)    # Date 타입
    last_login = models.DateTimeField(auto_now_add=True) # DateTime 타입
    receive_marketing = models.BooleanField() # 마케팅정보 수신여부. 0:미수신 1:수신

    class Meta:
        db_table = 'P2_user'
        verbose_name = '회원'
        verbose_name_plural = '회원(들)'
    
    # def __str__(self):
    #     return f'{self.u_id}:{self.username}|{self.name}|{self.nickname}|{self.email}|{self.address}|{self.mobile}' # 주문,배송에 자주 쓰일것 같은 필드만 표기하였습니다

class Cuppon(models.Model):
    discount_rate = models.FloatField() # 0.2, 0.3 같이 할인율은 소수로 표기하는게 좋을것 같아 float field로 작성했습니다.
    cuppon_num = models.IntegerField(default=0) # 개수
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def description(self):
        return f'{int(self.discount_rate * 100)}% 할인 쿠폰'

    class Meta:
        db_table = 'P2_cuppon'
        verbose_name = '쿠폰'
        verbose_name_plural = '쿠폰(들)'



class User_order(models.Model):
    ORDERSTATUS = (
        (1, '주문접수'),
        (2, '배송준비'),
        (3, '출고완료'),
        (4, '배송중'),
        (5, '배송완료'),
        (6, '주문취소'),
        (7, '교환/환불대기'),
        (8, '교환/환불완료'),
    )
    order_num = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    adress = models.CharField(max_length=200)
    receive_name = models.CharField(max_length=32)
    receive_phone = models.CharField(max_length=16)
    orderstatus = models.IntegerField(choices=ORDERSTATUS) # get_orderstatus_display 로 사용
    received_date = models.DateTimeField(null=True)
    
    class Meta:
       db_table = 'P2_User_order'
       verbose_name = '주문'
       verbose_name_plural = '주문(들)'
    

class Product_category(models.Model):
    category_code = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    class Meta:
       db_table = 'P2_Product_category'
       verbose_name = '상품카테고리'
       verbose_name_plural = '상품카테고리(들)'
    

class Product(models.Model):
    product_num = models.AutoField(primary_key=True)
    category_code = models.ForeignKey(Product_category, on_delete=models.PROTECT)
    product_price = models.IntegerField()
    product_name = models.CharField(max_length=50)
    product_stock = models.IntegerField(default=0)
    product_date = models.DateField(auto_now_add=True)
    # product_thumnail = models.ImageField(null=True, blank=True, upload_to='UploadedFiles/')
    # 템플릿에서 product_image 가공해서 사용
    product_rate = models.FloatField(default=0)
    product_image = models.ImageField(null=True, blank=True, upload_to='UploadedFiles')
    product_color = models.CharField(max_length=50, null=True) # 색상 # null 허용
    product_size = models.CharField(max_length=50, null=True)  # 사이즈 # null 허용    

    class Meta:
       db_table = 'P2_Product'
       verbose_name = '상품'
       verbose_name_plural = '상품(들)'


class User_order_detail(models.Model):
    product_num = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_num = models.ForeignKey(User_order, on_delete=models.CASCADE)
    product_count = models.IntegerField()
    product_price = models.IntegerField()

    class Meta:
        db_table = 'P2_User_order_detail'
        verbose_name = '주문상세정보'
        verbose_name_plural = '주문상세정보(들)'


class Grade(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_num = models.ForeignKey(Product, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])

    class Meta:
        db_table = 'P2_Grade'
        verbose_name = '상품평점'
        verbose_name_plural = '상품평점(들)'

    
class Cart(models.Model):
    product_num = models.ForeignKey(Product, on_delete=models.CASCADE)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_count = models.IntegerField()

    class Meta:
        db_table = 'P2_Cart'
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니(들)'

class Customer_inquiry(models.Model):
    c_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30) # 문의글 제목
    content = models.CharField(max_length=500)
    reg_date = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'P2_Customer_inquiry'
        verbose_name = '문의사항'
        verbose_name_plural = '문의사항(들)'
    
