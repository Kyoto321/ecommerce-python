from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify


from .models import Userprofile
from store.forms import ProductForm
from store.models import Product, Order, OrderItem
from .forms import RegisterUserForm

# Create your views here.
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products': products
    }) 


@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    # to get all order items
    order_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, 'userprofile/my_store.html', {
        'products': products,
    })

@login_required
def store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/store_order_detail.html', {
        'order': order
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)   # to displace an instance of a product without storing in the database 
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'Product has been added successfully.')

            return redirect('my_store')
    else:
        form = ProductForm()

    return render(request, 'userprofile/product.html', {
        'title': 'Add product',
        'form': form
    })


@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'Product has been updated successfully.')

        return redirect('my_store')
    else:
        form = ProductForm(instance=product)

    form = ProductForm(instance=product)

    return render(request, 'userprofile/product.html', {
        'title': 'Edit product',
        'product': product,
        'form': form
    })    

 
@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = product.DELETED
    product.save()

    messages.success(request, 'Product has been successfully deleted.')
    return redirect('my_store')


def myaccount(request):
    return render(request, 'userprofile/myaccount.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('indexpage')
        else:
            messages.success(request, ("There was an error"))
            return redirect('login')
    else:
        return render(request, 'userprofile/login.html')
 
  
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('indexpage')   


"""   
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            userprofile = Userprofile.objects.create(user=user)
            return redirect('indexpage')
    else:
        form = UserCreationForm()
    return render(request, 'userprofile/signup.html', {
        'form': form
    })  
"""  


def signup(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, ("Successfully registered"))
            return redirect('indexpage')
    else:
        form = RegisterUserForm()

    return render(request, 'userprofile/signup.html', {
        'form': form,
    })