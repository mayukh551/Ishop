from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.category import Category
from .models.product import Product
from .models.customer import Customer


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

def validateCustomer(customer):
    # form validation
    pswrd = str(customer.password)
    uc = False
    lc = False
    n = False
    for i in pswrd:
        if i.isupper():
            uc = True
        elif i.islower():
            lc = True
        elif i.isnumeric():
            n = True

    error_msg = None
    if not customer.first_name:
        error_msg = "First name required !"
    elif not customer.last_name:
        error_msg = "Last name required !"
    elif not customer.phone:
        error_msg = "Phone number required !"
    elif len(customer.password) < 8:
        error_msg = "Password must be atleast 8 characters long !"
    elif uc == False or lc == False or n == False:
        error_msg = "Password must contain atleast 1 upper-case alphabet, 1 lower-case alphabet and 1 number"
    elif not (customer.password == customer.repassword):
        error_msg = "Re-entered password is not same"
    elif customer.isExists():
        error_msg = "A user-account already exists with this email"

    return error_msg

def registerUser(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')
    repassword = postData.get('repassword')
    error_msg = None

    customer = Customer(first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        password=password,
                        repassword=repassword)
    error_msg = validateCustomer(customer)

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'email': email
    }

    # registration of the customer (saving profile)
    if not error_msg:
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('homepage')
        # return HttpResponse("sign up success")
    else:
        data = {
            'error': error_msg,
            'values': value
        }
        return render(request, 'signup.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)


