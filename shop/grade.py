from shop.models import Grade, Product

a = Product.objects.all().values('product_num', 'product_name')
Grade.objects.select_related('product_num_id')