from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import Customer
# import * imports all of my models, instead of specifying them one by one
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, email=form.cleaned_data.get('email'))
            login(request, user)
            return redirect('store')
    else:
        form = UserRegisterForm()
    return render(request, 'potterystore/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'potterystore/login.html', {'form': form})

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'potterystore/store.html', context)
# This 

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'potterystore/cart.html', context)

    # This is for the cart, and our cart page. If the user has made an account (is authenticated), and added items to their cart, but not checked out, this maintains the items in their cart upon their next visit to the site
    # Here I'm retrieving or creating an order for the authenticated user, retrieving all items associated with that order (anything that's been put into the cart)
    # so the argument checks if they're authenticated
    # then it retrieves the Customer object associated with the user (their data in the database, which includes the items in their cart)
    # if they already have products in their cart, it retrieves those, or it creates a new one 
    # then it retrieves all the items associated with that order
    
    # if the user is just an unlogged in guest, their items are just an empty list, nothing in their cart, cart displays a zero


def checkout(request):
    context = {}
    return render(request, 'potterystore/checkout.html', context)
    