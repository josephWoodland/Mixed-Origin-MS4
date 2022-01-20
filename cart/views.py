from django.shortcuts import render, redirect

# import tkinter to check the state of a checkbox

# Create your views here.
def cart(request):
    template = "cart/cart.html"
    context = {}
    return render(request, template, context)


def add_to_cart(request, item_id):

    quantity = int(request.POST.get("order-amount"))
    redirect_url = request.POST.get("redirect_url")
    cart = request.session.get("cart", {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session["cart"] = cart
    print(request.session["cart"])
    return redirect(redirect_url)
