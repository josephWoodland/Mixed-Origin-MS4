from django.shortcuts import render
from .models import Profile, PartnerProfile

# Create your views here.


def userProfile(request):
    template = "profiles/profile.html"
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, template, context)
