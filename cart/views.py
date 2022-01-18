from django.shortcuts import render

# Create your views here.
def cart(request):
    template = 'cart/cart.html'
    context = {

    }
    return render(request, template, context)