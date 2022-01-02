from django.shortcuts import render
from products.models import Product
# Create your views here.


def home(request):
    """
    View to return the home page
    """
    template = "home/home.html"
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, template, context)
