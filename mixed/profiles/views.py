from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, PartnerProfile, Wallet
from .forms import ProfileForm, PartnerProfileForm, WalletForm

# Create your views here.


def userProfile(request):
    profile = request.user.profile

    if profile.is_partner == False:
        template = "profiles/profile.html"
    else:
        template = "profiles/partner_profile.html"
    
    if request.method == "POST":
        profile.partner_application == True
        messages.success(request, "Your application request has been sent")
        return redirect("profile")
    
    id = profile.id
    partner_profile = PartnerProfile.objects.get(partner_id=id)
    context = {
        "profile": profile,
        "partner": partner_profile,
    }
    
    return render(request, template, context)


def editProfile(request, pk):
    template = 'profiles/edit_profile.html'
    profile = Profile.objects.get(id=pk)

    if profile.is_partner == True:
        partner_profile = PartnerProfile.objects.get(partner_id=pk)

    profile_form = ProfileForm(instance=profile)
    profile_partner_form = PartnerProfileForm(instance=partner_profile)

    context = {
        "profile": profile,
        "partner": partner_profile,
        "profile_form": profile_form,
        "profile_partner_form": profile_partner_form,
    }
    
    return render(request, template, context)


def deleteProfile(request, pk):
    template = "profiles/delete_profile.html"
    context = {}
    return render(request, template, context)


def userWallet(request, pk):
    template = 'profiles/wallet.html'