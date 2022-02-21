from webbrowser import get
from django.shortcuts import render, get_object_or_404
from products.models import Product
from products.views import product_list
from profiles.models import PartnerProfile
from home.helper import paginateProdcuts


from django.db.models import Q

# Create your views here.


def partners(request):
    """
    View to get a all the instances of of PartnerProfiles
    Can take in a search query to filter the instances
    """
    template = "partners/partners.html"
    partners = PartnerProfile.objects.all()
    custom_range, partners, paginator = paginateProdcuts(request, partners, 4)

    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    partners = PartnerProfile.objects.distinct().filter(
        Q(company_name__icontains=search_query)
    )

    context = {
        "partners": partners,
        "search_query": search_query,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    return render(request, template, context)


def partner_profile(request, slug):
    template = "partners/partner_profile.html"
    partner = get_object_or_404(PartnerProfile, slug=slug)

    context = {
        "partner": partner,
    }
    return render(request, template, context)


def partner_products(request, pk):
    template = "partners/partner_products.html"
    partner = get_object_or_404(PartnerProfile, id=pk)
    products = partner.product_set.all()
    custom_range, products, paginator = paginateProdcuts(request, products, 4)

    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    products = Product.objects.distinct().filter(
        Q(name__icontains=search_query) & Q(owner__exact=partner)
    )

    context = {
        "partner": partner,
        "products": products,
        "paginator": paginator,
        "custom_range": custom_range,
    }

    return render(request, template, context)
