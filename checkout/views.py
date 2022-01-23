from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
import random

# Create your views here.


def order_number_generator():
    return str(random.randint(10000000, 99999999))


def checkout(request):
    template = "checkout/checkout.html"
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "You have nothing in your cart!")
        return redirect("home")

    form = OrderForm()

    context = {"cart": cart, "form": form}
    return render(request, template, context)
