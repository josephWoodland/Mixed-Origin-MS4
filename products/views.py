from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from profiles.models import PartnerProfile
from .models import Product
from .forms import ProductForm

# Create your views here.

def products(request):
    template = "products/products.html"
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, template, context)


@login_required()
def addProduct(request, pk):
    template = "products/add_product.html"
    partner = PartnerProfile.objects.get(id=pk)
    form = ProductForm()
    context = {"form": form, "partner": partner}

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = partner
            product.save()
            messages.success(request, "You have added a new product to your store!")
            return redirect("product-list", pk=pk)

    return render(request, template, context)


def viewProduct(request, pk):
    template = "products/view_product.html"
    product = Product.objects.get(id=pk)
    partner_profile = None

    if request.user.is_authenticated:
        profile = request.user.profile
        id = profile.id
        if profile.is_partner == True:
            partner_profile = PartnerProfile.objects.get(partner_id=id)

    context = {
        "product": product,
        "partner_profile": partner_profile,
    }

    return render(request, template, context)


@login_required()
def productList(request, pk):
    template = "products/product_list.html"
    partner = PartnerProfile.objects.get(id=pk)
    products = partner.product_set.all()

    context = {
        "partner": partner,
        "products": products,
    }

    return render(request, template, context)


@login_required()
def editProduct(request, pk):
    template = "products/edit_product.html"
    product = Product.objects.get(id=pk)
    partner = product.owner
    partner_id = partner.id
    form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product,
    }

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated product details.")
            return redirect("product-list", pk=partner_id)

        errors = form.errors
        messages.error(request, errors)

    return render(request, template, context)


@login_required()
def deleteProduct(request, pk):
    template = "products/delete_product.html"
    return render(request, template)
