from django.shortcuts import render
from products.models import Product
from products.views import productList
from profiles.models import PartnerProfile

from django.db.models import Q

# Create your views here.


def partners(request):
    template = "partners/partners.html"
    partners = PartnerProfile.objects.all()
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    partners = PartnerProfile.objects.distinct().filter(
        Q(company_name__icontains=search_query)
    )

    context = {
        "partners": partners,
        "search_query": search_query,
    }
    return render(request, template, context)


def partnerProfile(request, pk):
    template = "partners/partner_profile.html"
    partner = PartnerProfile.objects.get(id=pk)
    context = {
        "partner": partner,
    }
    return render(request, template, context)


def partnerProducts(request, pk):
    template = "partners/partner_products.html"
    partner = PartnerProfile.objects.get(id=pk)

    products = partner.product_set.all()

    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    products = Product.objects.distinct().filter(
        Q(name__icontains=search_query) 
        & Q(owner__exact=partner)
    )
    
    context = {
        "partner": partner,
        "products": products,
    }

    return render(request, template, context)
