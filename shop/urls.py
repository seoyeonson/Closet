from django.urls import path
from shop import views

urlpatterns = [
    path('', views.main, name='main'),
    path('product/<int:pk>/', views.product, name='product'),
    path('mypage/', views.mypage, name='mypage'),
    path('cart/', views.cart, name='cart'),
]
