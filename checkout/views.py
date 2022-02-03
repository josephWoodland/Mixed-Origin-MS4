from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import OrderForm
from .models import Order, OrderItem
from django.conf import settings
from django.contrib import messages
from products.models import Product
from profiles.forms import WalletForm
from profiles.models import Profile, Wallet
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
    user = request.user

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

            return redirect(reverse("checkout_success", args=[order.id]))

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

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            wallet = Wallet.objects.get(owner=profile)
            full_name = profile.first_name + " " + profile.second_name

            form = OrderForm(
                initial={
                    "full_name": full_name,
                    "email": profile.email,
                    "phone_number": wallet.phone_number,
                    "country": wallet.country,
                    "postcode": wallet.postcode,
                    "town_or_city": wallet.town_or_city,
                    "street_address1": wallet.street_address1,
                    "street_address2": wallet.street_address2,
                    "county": wallet.county,
                }
            )

        except Profile.DoesNotExist:
            form = OrderForm()

    else:
        form = OrderForm()

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
    profile = Profile.objects.get(user=request.user)
    wallet = Wallet.objects.get(owner=profile)
    order = get_object_or_404(Order, id=pk)
    order.profile = profile
    order.save()

    if walletDetails:

        wallet_data = {
            "country": order.country,
            "postcode": order.postcode,
            "town_or_city": order.town_or_city,
            "street_address1": order.street_address1,
            "street_address2": order.street_address2,
            "county": order.county,
        }

        profile_wallet_form = WalletForm(wallet_data, instance=wallet)
        if profile_wallet_form.is_valid():
            profile_wallet_form.save()

    messages.success(request, "Your order has been processed")

    if "cart" in request.session:
        del request.session["cart"]

    context = {
        "profile": profile,
        "order": order,
    }

    return render(request, template, context)


@login_required()
def previous_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    profile = order.profile
    template = "checkout/checkout_success.html"
    date = order.created.strftime("%Y-%m-%d")

    messages.info(
        request,
        (
            f"This is a previous order, \
            conformation email was sent on { date }."
        ),
    )

    context = {
        "order": order,
        "previous_order": True,
        "profile": profile,
    }

    return render(request, template, context)
