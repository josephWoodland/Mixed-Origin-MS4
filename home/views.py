from tempfile import template
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
        "products": products,
    }

    return render(request, template, context)


def blog(request):
    template = "home/blog.html"
    return render(request, template)


def about(request):
    template = "home/about_us.html"
    return render(request, template)
