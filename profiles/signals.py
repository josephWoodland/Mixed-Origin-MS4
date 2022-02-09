from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, PartnerProfile, Wallet
from django.conf import settings
from django.utils.text import slugify


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
        )


def createPartner(sender, instance, created, **kwargs):
    profile = instance

    if profile.is_partner:
        partner = PartnerProfile.objects.create(partner=profile)


def createWallet(sender, instance, created, **kwargs):
    if created:
        profile = instance
        name = profile.first_name
        wallet = Wallet.objects.create(owner=profile, name=name)


def partnerRequest(sender, instance, created, **kwargs):

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


def createPartnerSlug(sender, instance, created, **kwargs):

    partner = get_object_or_404(PartnerProfile, id=instance.id)
    slug = partner.slug

    if not created:
        if slug is None:
            id = partner.id.hex
            id_splice = id[0:8]
            name = slugify(partner.company_name)
            slug_str = f'{id_splice}-{name}'

            PartnerProfile.objects.filter(id=instance.id).update(slug=slug_str)


post_save.connect(createPartnerSlug, sender=PartnerProfile)
post_save.connect(createPartner, sender=Profile)
post_save.connect(createWallet, sender=Profile)
post_save.connect(createProfile, sender=User)
