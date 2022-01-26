from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderItem
from cart.contexts import cart_contents

import json
import stripe


def checkout(request):

    template = "checkout/checkout.html"
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get("cart", {})
    form = OrderForm()

    if not cart:

        messages.error(request, "You have nothing in your cart!")
        return redirect("home")

    if request.method == "POST":

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "county": request.POST["county"],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():

            order = order_form.save(commit=False)
            client_secret = request.POST.get("client_secret")
            pid = client_secret.split("_secret")[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            for item_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=item_id)
                item_total = product.price * quantity

                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    item_total=item_total,
                )

                order_item.save()

    else:

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

    context = {
        "cart": cart,
        "form": form,
        "stripe_public_key": stripe_public_key,
        "client_secret": client_secret,
    }

    return render(request, template, context)
