from django.shortcuts import render

from .models import Product

# Create your views here.
def addProduct(request):
    template = "products/add_product.html"
    context = {}
    return render(request, template, context)


def viewProduct(request, pk):
    template = 'products/view_product.html'
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }

    return render(request, template, context)