from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# import * imports all of my models, instead of specifying them one by one
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

def registerPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'potterystore/register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username or Password is incorrect')
        
        
    context = {}
    return render(request, 'potterystore/login.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('login')

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
    