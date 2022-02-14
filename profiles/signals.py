from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, PartnerProfile, Wallet
from django.conf import settings
from django.utils.text import slugify


def create_profile(sender, instance, created, **kwargs):
    """
    Signal to create a profile on the creation of User
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
        )


def create_partner(sender, instance, created, **kwargs):
    """
    Creates a PartnerProfile when the admin accepts
    the Profile application to sell items on the site
    """
    profile = instance

    if profile.is_partner:
        partner = PartnerProfile.objects.create(partner=profile)


def create_wallet(sender, instance, created, **kwargs):
    """
    Creates a wallet instance on the creation of a profile model
    """
    if created:
        profile = instance
        name = profile.first_name
        wallet = Wallet.objects.create(owner=profile, name=name)


def partner_request(sender, instance, created, **kwargs):
    """
    Sends a email instance triggered Profile on request
    of the profile by selecting True for the partner application
    attr in the profile class
    """

    profile = instance
    partner_request = profile.partner_application
    is_partner = profile.is_partner

    if partner_request == True and is_partner == False:
        email = settings.DEFAULT_FROM_EMAIL

        subject = render_to_string(
            "profiles/email_request/email_request_subject.txt",
            {"profile": profile},
        )
        body = render_to_string(
            "profiles/email_request/email_request_body.txt",
            {"profile": profile},
        )

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])


def partner_request(sender, instance, created, **kwargs):
    """
    Sends a email instance triggered by the acceptance of a partner Application
    """

    profile = instance
    is_partner = profile.is_partner
    partner_email = profile.partner_email_sent
    email = profile.email

    if is_partner == True and partner_email == False:

        subject = render_to_string(
            "profiles/email_request/partner_accepted_subject.txt",
            {"profile": profile},
        )
        body = render_to_string(
            "profiles/email_request/partner_accepted_body.txt",
            {"profile": profile},
        )

        partner_email = True

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])


def create_partner_slug(sender, instance, created, **kwargs):
    """
    Creates a Slug for a Partner profile on creation
    which is used as the url for partner profile page
    """
    partner = get_object_or_404(PartnerProfile, id=instance.id)
    slug = partner.slug

    if not created:
        if slug is None or len(slug) < 4:
            id = partner.id.hex
            id_splice = id[0:8]
            name = slugify(partner.company_name)
            slug_str = f"{id_splice}-{name}"

            PartnerProfile.objects.filter(id=instance.id).update(slug=slug_str)


post_save.connect(create_partner_slug, sender=PartnerProfile)
post_save.connect(create_partner, sender=Profile)
post_save.connect(create_wallet, sender=Profile)
post_save.connect(create_profile, sender=User)
