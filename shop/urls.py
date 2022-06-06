from django.urls import path
from shop import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main, name='main'),
    path('list/<int:cg>/', views.list, name='list'),
    path('product/<str:name>/', views.product, name='product'),
    path('mypage/', views.mypage, name='mypage'),
    path('cart/', views.cart, name='cart'),
    path('test_images/<int:id>/', views.test_images),
]

urlpatterns += static(
    settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT
)