from django.contrib import admin
from django.contrib import admin
from .models import Profile, PartnerProfile, Wallet

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    """
    Settings for the Profile admin
    """

    list_display = ("username", "email", "partner_application")
    list_display_links = ("username",)


class PartnerProfileAdmin(admin.ModelAdmin):
    """
    Settings for the PartnerProfile admin
    """

    list_display = ("id", "company_name", "partner")
    list_display_links = ("id", "company_name", "partner")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(PartnerProfile, PartnerProfileAdmin)
admin.site.register(Wallet)
