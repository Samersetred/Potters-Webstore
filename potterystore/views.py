from django.http import HttpResponse
from .models import *
# import * imports all of my models, instead of specifying them one by one

# ley login and logout imports
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

# key javascript imports
from django.http import JsonResponse
import json

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

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for non-logged in users
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
            
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'potterystore/store.html', context)
# This 

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
    # this parses the request data

	customer = request.user.customer
	product = Product.objects.get(id=productId)
    # this retrieves the customer info and product

	order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # this retrieves, if products have already been ordered, or creates the order

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # this retrieves, if products have already been ordered, or creates the order item

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
    # this updates the order item quantity

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
    # this saves or deletes the order item

	return JsonResponse('Item was added', safe=False)
    # this returns a Json response 'Item was added'

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'potterystore/cart.html', context)

    # This is for the cart, and our cart page. If the user has made an account (is authenticated), and added items to their cart, but not checked out, this maintains the items in their cart upon their next visit to the site
    # Here I'm retrieving or creating an order for the authenticated user, retrieving all items associated with that order (anything that's been put into the cart)
    # so the argument checks if they're authenticated
    # then it retrieves the Customer object associated with the user (their data in the database, which includes the items in their cart)
    # if they already have products in their cart, it retrieves those, or it creates a new one 
    # then it retrieves all the items associated with that order
    # if the user is just an unlogged in guest, their items are just an empty list, nothing in their cart, cart displays a zero


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    # This is for the empty cart for now for non-logged in user

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'potterystore/checkout.html', context)
    