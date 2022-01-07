from django.shortcuts import render

from profiles.models import Profile, PartnerProfile
from .models import Product
from .forms import ProductForm

# Create your views here.
def addProduct(request):
    template = "products/add_product.html"
    form = ProductForm()
    context = {"form": form}
    return render(request, template, context)


def viewProduct(request, pk):
    template = "products/view_product.html"
    product = Product.objects.get(id=pk)
    context = {
        "product": product,
    }

    return render(request, template, context)


def productList(request, pk):
    template = "products/product_list.html"
    partner = PartnerProfile.objects.get(id=pk)
    products = partner.product_set.all()

    context = {
        'partner': partner,
        'products': products,
    }

    return render(request, template, context)


def editProduct(request, pk):
    template = 'products/edit_product'
    return render(request, template)


def deleteProduct(request, pk):
    template = 'products/edit_product'
    return render(request, template)
