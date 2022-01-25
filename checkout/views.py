from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    template = "checkout/checkout.html"
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "You have nothing in your cart!")
        return redirect("home")

    form = OrderForm()

    context = {"cart": cart, "form": form}
    return render(request, template, context)
