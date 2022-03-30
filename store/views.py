from django.shortcuts import render
from django.http import HttpResponse

from .models.product import Product
# Create your views here.

def index(request):
    prod=Product.get_all_products()
    print(prod)
    return render(request, 'index.html', {'products':prod})