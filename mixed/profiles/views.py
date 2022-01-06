from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, PartnerProfile, Wallet
from .forms import ProfileForm, PartnerProfileForm, WalletForm

# Create your views here.


def userProfile(request):
    template = "profiles/profile.html"
    profile = request.user.profile

    if request.method == "POST":
        profile.partner_application = True
        messages.success(request, "Your application request has been sent")
        return redirect("profile")
    
    id = profile.id
    partner_profile = PartnerProfile.objects.get(partner_id=id)
    profile_wallet = Wallet.objects.get(owner_id=id)
    context = {
        "profile": profile,
        "partner": partner_profile,
        "wallet": profile_wallet,
    }
    

    
    return render(request, template, context)


def editProfile(request):
    template = 'profiles/edit_profile.html'
    profile = request.user.profile
    partner_profile = PartnerProfile.objects.get(partner_id=id)
    profile_wallet = Wallet.objects.get(owner_id=id)
    profile_form = ProfileForm
    profile_partner_form = PartnerProfileForm
    wallet_form = WalletForm
    context = {
        "profile": profile,
        "partner": partner_profile,
        "wallet": profile_wallet,
        "profile_form": profile_form,
        "profile_partner_form": profile_partner_form,
        "wallet_form": wallet_form,
    }
    return render(request, template, context)


def deleteProfile(request):
    template = "profiles/delete_profile.html"
    context = {}
    return render(request, template, context)


def userWallet(request, pk):
    template = 'profiles/wallet.html'