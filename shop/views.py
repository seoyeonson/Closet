from django.shortcuts import render

def main(request):
    return render(request, 'index.html')

def product(request, pk):
    return render(request, 'product.html')

def mypage(request):
    return render(request, 'mypage.html')

def cart(request):
    return render(request, 'cart.html')