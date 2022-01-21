from django.shortcuts import render
import random

# Create your views here.


def order_number_generator():
    return str(random.randint(10000000, 99999999))


def checkout(request):
    template = "checkout/checkout.html"
    context = {}
    return render(request, template, context)
