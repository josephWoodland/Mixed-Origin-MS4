from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    template = "checkout/checkout.html"
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "You have nothing in your cart!")
        return redirect("home")

    form = OrderForm()

    context = {
        "cart": cart,
        "form": form,
        "stripe_public_key": stripe_public_key,
        "client_secret": 8,
    }
    return render(request, template, context)
