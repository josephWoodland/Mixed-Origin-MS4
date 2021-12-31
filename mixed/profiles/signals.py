from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile, PartnerProfile


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
        partner = PartnerProfile.objects.create(
            partner=profile
        )


post_save.connect(createPartner, sender=Profile)
post_save.connect(createProfile, sender=User)
