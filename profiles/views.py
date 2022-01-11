from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, PartnerProfile, Wallet
from .forms import ProfileForm, PartnerProfileForm, WalletForm

# Create your views here.


@login_required()
def userProfile(request):
    profile = request.user.profile

    if profile.is_partner == False:
        template = "profiles/profile.html"
        partner_profile = None
    else:
        template = "profiles/partner_profile.html"
        partner_profile = PartnerProfile.objects.get(partner_id=id)

    if request.method == "POST":
        profile.partner_application == True
        messages.success(request, "Your application request has been sent")
        return redirect("profile")

    id = profile.id
    context = {
        "profile": profile,
        "partner": partner_profile,
    }

    return render(request, template, context)


@login_required()
def editProfile(request, pk):
    template = "profiles/edit_profile.html"
    profile = Profile.objects.get(id=pk)
    partner_profile = None

    if profile.is_partner == True:
        partner_profile = PartnerProfile.objects.get(partner_id=pk)

    profile_form = ProfileForm(instance=profile)

    context = {
        "profile": profile,
        "partner": partner_profile,
        "profile_form": profile_form,
    }

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, "You have edited your profile!")
            return redirect("home")

        errors = form.errors
        messages.error(request, errors)

    return render(request, template, context)


@login_required()
def editPartner(request, pk):
    template = "profiles/edit_partner.html"
    partner_profile = PartnerProfile.objects.get(id=pk)
    partner_form = PartnerProfileForm(instance=partner_profile)

    context = {
        "partner_profile": partner_profile,
        "partner_form": partner_form,
    }

    if request.method == "POST":
        partner_form = PartnerProfileForm(
            request.POST, request.FILES, instance=partner_profile
        )
        if partner_form.is_valid():
            partner_form.save()

            messages.success(request, "You have updated your account")
            return redirect("profile")

        errors = partner_form.errors
        messages.error(request, errors)

    return render(request, template, context)


@login_required()
def deleteProfile(request, pk):
    template = "profiles/delete_profile.html"
    context = {}
    return render(request, template, context)


@login_required()
def userWallet(request, pk):
    template = "profiles/wallet.html"
    return render(request, template)
