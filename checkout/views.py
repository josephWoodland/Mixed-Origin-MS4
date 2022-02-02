from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST

from django.conf import settings
from django.contrib import messages
from products.models import Product
from profiles.models import Profile
from .forms import OrderForm
from .models import Order, OrderItem
from cart.contexts import cart_contents

import json
import stripe


@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get("client_secret")
        pid = client_secret.split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        walletDetails = request.POST.get("walletDetails")

        print("----- Wallet Save ----- : ", walletDetails)
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "cart": json.dumps(request.session.get("cart", {})),
                "walletDetails": walletDetails,
                "username": request.user,
            },
        )
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(
            request,
            "Sorry, there was an issue with your \
            payment. Please try again later.",
        )
        return HttpResponse(content=e, status=400)


def checkout(request):

    template = "checkout/checkout.html"
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get("cart", {})
    form = OrderForm()
    user = request.user
    profile = None
    wallet = None

    if user:

        profile = Profile.objects.get(user=user)

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
                try:
                    product = get_object_or_404(Product, pk=item_id)
                    item_total = product.price * quantity

                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        item_total=item_total,
                    )

                    order_item.save()

                except Product.DoesNotExist:
                    messages.error(
                        request,
                        (
                            "One of the products in your bag wasn't found in our database. "
                            "Please call us for assistance!"
                        ),
                    )
                    order.delete()
                    return redirect(reverse("cart"))

            request.session["walletDetails"] = "walletDetails" in request.POST

            return redirect(reverse("checkout_success", args=[order.order_number]))

        else:
            messages.error(
                request,
                "There was an error with your form. \
                Please check your information again.",
            )
    else:

        cur_cart = cart_contents(request)

        if not cart:

            messages.error(request, "You have nothing in your cart!")
            return redirect("home")

        cart_total = cur_cart["grand_total"]
        stripe_total = round(cart_total * 100)
        stripe.api_key = stripe_secret_key

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    client_secret = intent.client_secret

    context = {
        "cart": cart,
        "form": form,
        "stripe_public_key": stripe_public_key,
        "client_secret": client_secret,
    }

    return render(request, template, context)


def checkout_success(request, pk):
    template = "checkout/checkout_success.html"
    walletDetails = request.session.get("walletDetails")
    order = get_object_or_404(Order, order_number=pk)
    profile = order.profile
    messages.success(request, "Your order has been processed")

    if "cart" in request.session:
        del request.session["cart"]

    context = {
        "profile": profile,
        "order": order,
    }

    return render(request, template, context)
