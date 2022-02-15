from django.shortcuts import render, redirect, reverse
from django.template import Origin
from products.models import Product
from django.contrib import messages

import time

# Create your views here.


def cart(request):
    """
    View calls renders the cart template
    """
    template = "cart/cart.html"
    context = {}

    return render(request, template, context)


def add_to_cart(request, item_id):
    """This view adds a product to the current session cart

    Args:
        item_id (id): This is the product id

    Returns:
        [session object]: Returns an updated cart object to the session cookie
    """
    print("This should be an id: ----- ", item_id)
    print("------------------------------------------------------------")
    product = Product.objects.get(id=item_id)
    quantity = request.POST.get("order-amount")
    # If order does not come from the product view order set to 1
    if quantity is None:
        quantity = 1

    current_stock = product.stock_numbers
    new_stock = current_stock - int(quantity)
    product.stock_numbers = new_stock

    if new_stock == 0:
        product.in_stock = False

    product.save()

    redirect_url = request.POST.get("redirect_url")

    if redirect_url is None:
        redirect_url = "home"

    cart = request.session.get("cart", {})

    if item_id in list(cart.keys()):
        cart[item_id] += int(quantity)
    else:
        cart[item_id] = int(quantity)

    request.session["cart"] = cart

    time.sleep(1)

    return redirect(redirect_url)


def update_cart(request, pk):
    """
    Updates the cart with the items and
    adjust the stock amount for a given product in the database
    """
    product = Product.objects.get(id=pk)
    id = pk
    new_amount = int(request.POST.get("cart-amount"))
    current_stock = product.stock_numbers
    cart = request.session.get("cart", {})
    current_amount = cart[id]
    total_stock = current_stock + current_amount
    current_stock = total_stock - new_amount
    product.stock_numbers = current_stock
    product.save()
    cart[id] = new_amount
    messages.success(
        request, f"You have updated { product.name } in your cart!")

    request.session["cart"] = cart

    return redirect(reverse("cart"))


def delete_cart_item(request, pk):
    """
    Updates the cart when Item is deleted,
    alters the product stock amount in the database
    """
    product = Product.objects.get(id=pk)
    cart = request.session.get("cart", {})
    id = pk
    current_stock = product.stock_numbers
    order_number = cart[id]
    product.stock_numbers = current_stock + order_number
    product.save()
    del cart[id]
    messages.success(
        request, f"You have deleted { product.name } from your cart!")
    request.session["cart"] = cart

    return redirect(reverse("cart"))
