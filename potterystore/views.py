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

def cart(request):
    context = {}
    return render(request, 'potterystore/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'potterystore/checkout.html', context)
    