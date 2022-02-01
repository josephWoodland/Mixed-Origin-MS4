from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, PartnerProfile, Wallet


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

    profile = instance
    name = profile.first_name
    wallet = Wallet.objects.create(owner=profile, name=name)


post_save.connect(createPartner, sender=Profile)
post_save.connect(createWallet, sender=Profile)
post_save.connect(createProfile, sender=User)
