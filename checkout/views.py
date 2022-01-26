from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm
from cart.contexts import cart_contents
import stripe


def checkout(request):
    template = "checkout/checkout.html"
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get("cart", {})
    cur_cart = cart_contents(request)
    cart_total = cur_cart["grand_total"]
    stripe_total = round(cart_total * 100)
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    client_secret = intent.client_secret

    if not cart:
        messages.error(request, "You have nothing in your cart!")
        return redirect("home")

    form = OrderForm()

    context = {
        "cart": cart,
        "form": form,
        "stripe_public_key": stripe_public_key,
        "client_secret": client_secret,
    }
    return render(request, template, context)
