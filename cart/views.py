from django.shortcuts import render, redirect, reverse
from products.models import Product
# import tkinter to check the state of a checkbox

# Create your views here.
def cart(request):
    template = "cart/cart.html"
    context = {}
    return render(request, template, context)


def add_to_cart(request, item_id):
    product = Product.objects.get(id=item_id)
    quantity = int(request.POST.get("order-amount"))
    current_stock = product.stock_numbers
    new_stock = current_stock - quantity
    product.stock_numbers = new_stock

    if new_stock == 0:
        product.in_stock = False
    
    product.save()

    redirect_url = request.POST.get("redirect_url")
    cart = request.session.get("cart", {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session["cart"] = cart

    return redirect(redirect_url)


def update_cart(request, pk):
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

    request.session["cart"] = cart

    return redirect(reverse('cart'))


def delete_cart_item(request, pk):
    id = pk
    cart = request.session.get("cart", {})
    cart[id] = 0
    request.session["cart"] = cart

    return redirect(reverse('cart'))