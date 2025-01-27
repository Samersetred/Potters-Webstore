from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# import * imports all of my models, instead of specifying them one by one

# Create your views here.

# def home_page_view(request):
#    return HttpResponse('Hello, Worldies')

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'potterystore/store.html', context)
# This 

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        #empty cart
        items = []

    # This is for the cart, and our cart page. If the user has made an account (is authenticated), and added items to their cart, but not checked out, this maintains the items in their cart upon their next visit to the site
    # Here I'm retrieving or creating an order for the authenticated user, retrieving all items associated with that order (anything that's been put into the cart)
    # so the argument checks if they're authenticated
    # then it retrieves the Customer object associated with the user (their data in the database, which includes the items in their cart)
    # if they already have products in their cart, it retrieves those, or it creates a new one 
    # then it retrieves all the items associated with that order
    
    # if the user is just an unlogged in guest, their items are just an empty list, nothing in their cart, cart displays a zero

    context = {'items':items}
    return render(request, 'potterystore/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'potterystore/checkout.html', context)
    