from django.contrib import admin
from .models import User, Product, Product_category, Cart, User_order, User_order_detail
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Product_category)