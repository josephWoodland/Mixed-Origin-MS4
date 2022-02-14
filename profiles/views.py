from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Profile, PartnerProfile, Wallet
from .forms import ProfileForm, PartnerProfileForm, WalletForm

# Create your views here.


@login_required(login_url="/accounts/login/")
def user_profile(request):
    """This is the main profile view

    Args:
        request (GET): This view takes in the user profile status

    Returns:
        [render html]: Using the profile status of the account
         the view renders the necessary template for that user.
    """
    profile = request.user.profile
    id = profile.id

    # Checks the status of the user profile to return the correct template
    if profile.is_partner is False:
        template = "profiles/profile.html"
        partner_profile = None
    else:
        partner_profile = PartnerProfile.objects.get(partner_id=id)
        if partner_profile.company_name == "":
            return redirect("edit-partner", pk=partner_profile.id)

        template = "partners/partner_profile.html"

    if request.method == "POST":
        form = request.POST
        if ("partner_application") in form:
            profile = Profile.objects.filter(id=id)
            profile.update(partner_application=True)
            # Sends admin a email on the partner request
            user = request.user.profile
            email = settings.DEFAULT_FROM_EMAIL

            subject = render_to_string(
                "profiles/email_request/email_request_subject.txt",
                {"profile": user},
            )
            body = render_to_string(
                "profiles/email_request/email_request_body.txt",
                {"profile": user},
            )

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "Your application request has been sent")
            return redirect("profile")
        else:
            messages.error(request, "Please check the radio button to apply.")
            return redirect("profile")

    context = {
        "profile": profile,
        "partner": partner_profile,
    }

    return render(request, template, context)


@login_required()
def edit_profile(request, pk):
    """
    This is the view to edit a user profile
    """
    template = "profiles/edit_profile.html"
    profile = Profile.objects.get(id=pk)
    partner_profile = None

    if profile.is_partner is True:
        # checks if the profile is a partner
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
            form.save()
            messages.success(request, "You have edited your profile!")
            return redirect("home")

        errors = form.errors
        messages.error(request, errors)

    return render(request, template, context)


@login_required()
def edit_partner(request, pk):
    """
    This view edits the partner profile
    """
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
            return redirect("home")

        errors = partner_form.errors
        messages.error(request, errors)

    return render(request, template, context)


@login_required()
def delete_profile(request, pk):
    """
    Deletes the profile object
    """
    template = "includes/delete_template.html"
    profile = request.user.profile

    if request.method == "POST":
        user = request.user
        user.delete()
        profile.delete()
        messages.success(request, "Your profile has been deleted!")
        logout(request)
        return redirect("home")

    context = {"object": profile}

    return render(request, template, context)


@login_required()
def user_wallet(request, pk):
    """
    Displays the user wallet data
    """
    template = "profiles/wallet.html"
    profile = Profile.objects.get(id=pk)
    wallet = Wallet.objects.get(owner=profile)

    if wallet:
        form = WalletForm(instance=wallet)
    else:
        form = WalletForm()

    if request.method == "POST":
        profile = profile
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            messages.success(request, "You have saved your wallet data.")

        return redirect("profile")

    context = {"form": form, "profile": profile, "wallet": wallet}

    return render(request, template, context)


@login_required()
def orders(request, pk):
    """
    Displays the user previous orders
    """
    template = "profiles/orders.html"
    profile = Profile.objects.get(id=pk)
    orders = profile.orders.all()

    context = {
        "profile": profile,
        "orders": orders,
    }

    return render(request, template, context)
