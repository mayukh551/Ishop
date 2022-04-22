from django.shortcuts import render
from store.models.category import Category
from store.models.product import Product


# Create your views here.

def index(request):
    products = None
    categories = Category.get_all_categories()
    category_ID = request.GET.get('category')
    if category_ID:
        products = Product.get_all_products_id(category_ID)
    else:
        products = Product.get_all_products()
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'index.html', data)
