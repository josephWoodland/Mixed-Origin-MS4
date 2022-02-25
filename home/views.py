from django.shortcuts import get_object_or_404, render
from home.helper import paginateProdcuts
from products.models import Product
from profiles.models import PartnerProfile

# Create your views here.


def home(request):
    """
    View to return the home page
    """
    template = "home/home.html"
    products = Product.objects.all()
    custom_range, products, paginator = paginateProdcuts(
        request, products, 4)

    promoted_partner = get_object_or_404(PartnerProfile, promoted=True)

    if not promoted_partner:
        promoted_partner = None

    context = {
        "products": products,
        "paginator": paginator,
        "custom_range": custom_range,
        "promoted_partner": promoted_partner,
    }

    return render(request, template, context)


def blog(request):
    """
    View to return the Blog pages
    """
    template = "home/blog.html"
    return render(request, template)


def about(request):
    """
    View to return the About page
    """
    template = "home/about_us.html"
    return render(request, template)
