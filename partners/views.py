from django.shortcuts import render
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
    template = "partners/partner-profile.html"
    context = {
        
    }
    return render(request, template, context)