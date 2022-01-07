from django.shortcuts import redirect, render
from django.contrib import messages

from profiles.models import Profile, PartnerProfile
from .models import Product
from .forms import ProductForm

# Create your views here.
def addProduct(request, pk):
    template = "products/add_product.html"
    partner = PartnerProfile.objects.get(id=pk)
    form = ProductForm()
    context = {"form": form, "partner":partner}

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = partner
            product.save()
            messages.success(request, 'You have added a new product to your store!')
            return redirect("product-list", pk=pk)

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
