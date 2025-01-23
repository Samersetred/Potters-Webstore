from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# def home_page_view(request):
#    return HttpResponse('Hello, Worldies')

def store(request):
    context = {}
    return render(request, 'potterystore/store.html', context)

def cart(request):
    context = {}
    return render(request, 'potterystore/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'potterystore/checkout.html', context)
    