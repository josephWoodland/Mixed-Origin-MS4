from email.mime import image
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from profiles.models import PartnerProfile
from .models import Product, Tag
from .forms import ProductForm
from django.db.models import Q
from home.helper import paginateProdcuts
from django.conf import settings

import os
from mixed.settings import MEDIA_URL, MEDIA_ROOT

# Create your views here.


def products(request):
    """
    Product view which handels data from the products query set
    takes in a search query in request to fillter through the Products Objects
    """
    template = "products/products.html"
    products = Product.objects.all()
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)

    products = Product.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__company_name__icontains=search_query) |
        Q(tags__in=tags)
    )

    custom_range, products, paginator = paginateProdcuts(request, products, 8)

    context = {
        "products": products,
        "search_query": search_query,
        "custom_range": custom_range,
        "paginator": paginator,
    }

    return render(request, template, context)


def product_tags(request, tag):
    """
    View to filter products by product tags
    """
    template = "products/products.html"
    products = Product.objects.all()
    tags = Tag.objects.filter(name__icontains=tag)
    products = Product.objects.distinct().filter(Q(tags__in=tags))

    context = {
        "products": products,
    }

    return render(request, template, context)


@login_required()
def add_product(request, pk):
    """
    View to add products to the database, can only ba accessed by Partners
    """
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
            messages.success(
                request, "You have added a new product to your store!")
            return redirect("product-list", pk=pk)

    return render(request, template, context)


def view_product(request, slug):
    """
    View to grab a specific product from the database
    and pass it into the view. Takes in a slug to search the database
    via passing it through the url
    """
    template = "products/view_product.html"
    product = get_object_or_404(Product, slug=slug)
    partner_profile = None
    products = Product.objects.all()

    # Check to see if product has tags
    if len(product.tags.all()) > 0:
        # Get the first Tag
        tag = product.tags.all()[0]
        # Search items with that tag
        tags = Tag.objects.filter(name__icontains=tag)
        products = Product.objects.distinct().filter(Q(tags__in=tags))

    custom_range, products, paginator = paginateProdcuts(request, products, 4)

    if request.user.is_authenticated:
        profile = request.user.profile
        id = profile.id
        if profile.is_partner is True:
            partner_profile = PartnerProfile.objects.get(partner_id=id)

    context = {
        "product": product,
        "partner_profile": partner_profile,
        "products": products,
        "paginator": paginator,
        "custom_range": custom_range,
    }

    return render(request, template, context)


@login_required()
def product_list(request, pk):
    """
    View which filters the database for products
    by partner. Item found by the pk which is the product id
    """
    template = "products/product_list.html"
    partner = PartnerProfile.objects.get(id=pk)
    products = partner.product_set.all()

    context = {
        "partner": partner,
        "products": products,
    }

    return render(request, template, context)


@login_required()
def edit_product(request, pk):
    """
    View to edit specific product, search by product id
    """
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
def delete_product(request, pk):
    """
    View to delete product from the database, view searches the product by id
    """
    template = "includes/delete_template.html"
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product has been deleted!")
        return redirect("profile")

    context = {"object": product}

    return render(request, template, context)
