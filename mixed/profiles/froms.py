from django.db import models
from django.forms import ModelForm
from django import forms

from .models import Profile, PartnerProfile, Wallet


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "second_name",
            "email",
            "profile_image" "partner_application",
        ]

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)

            for name, fields in self.fields.items():
                names = name.capitalize()
                fields.widget.attrs.update({"class": "input", "placeholder": names})


class PartnerProfileForm(forms.ModelForm):
    class Meta:
        model = PartnerProfile
        fields = [
            "company_name",
            "company_website",
            "company_short_bio",
            "company_description",
            "social_twitter",
            "social_linkedin",
            "social_youtube",
            "social_website",
        ]

        def __init__(self, *args, **kwargs):
            super(PartnerProfileForm, self).__init__(*args, **kwargs)

            for name, fields in self.fields.items():
                names = name.capitalize()
                fields.widget.attrs.update({"class": "input", "placeholder": names})


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = [
            "name",
            "street_address1",
            "street_address2",
            "town_or_city",
            "county",
            "postcode",
            "country",
        ]

        def __init__(self, *args, **kwargs):
            super(WalletForm, self).__init__(*args, **kwargs)

            for name, fields in self.fields.items():
                names = name.capitalize()
                fields.widget.attrs.update({"class": "input", "placeholder": names})
