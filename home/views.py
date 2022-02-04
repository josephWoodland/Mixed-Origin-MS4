from django.shortcuts import render
from home.helper import paginateProdcuts
from products.models import Product

# Create your views here.


def home(request):
    """
    View to return the home page
    """
    template = "home/home.html"
    products = Product.objects.all()
    custom_range, products, paginator = paginateProdcuts(request, products, 4)

    context = {
        "products": products,
        "paginator": paginator,
        "custom_range": custom_range,
    }

    return render(request, template, context)


def blog(request):
    template = "home/blog.html"
    return render(request, template)


def about(request):
    template = "home/about_us.html"
    return render(request, template)
