from django import forms

from .models import Profile, PartnerProfile, Wallet


class ProfileForm(forms.ModelForm):
    class Meta:

        model = Profile

        fields = [
            "first_name",
            "second_name",
            "email",
            "profile_image",
            "partner_application",
        ]

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            placeholders = {
                "first_name": "First Name",
                "second_name": "Second Name",
                "email": "Email",
            }

            for fields in self.fields.items():

                fields.widget.attrs.update(
                    {"class": "input", "placeholder": placeholders}
                )


class PartnerProfileForm(forms.ModelForm):
    class Meta:
        model = PartnerProfile
        fields = [
            "company_image",
            "company_name",
            "company_website",
            "company_short_bio",
            "company_description",
            "social_twitter",
            "social_linkedin",
            "social_youtube",
        ]

        def __init__(self, *args, **kwargs):
            super(PartnerProfileForm, self).__init__(*args, **kwargs)
            placeholders = {
                "company_name": "Company Name",
                "company_website": "Company URL",
                "company_short_bio": "Company Strapline",
                "company_description": "Description",
                "social_twitter": "Twitter",
                "social_linkedin": "LinkedIn",
                "social_youtube": "You Tube",
            }

            for fields in self.fields.items():

                fields.widget.attrs.update(
                    {"class": "input", "placeholder": placeholders}
                )


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = [
            "phone_number",
            "street_address1",
            "street_address2",
            "town_or_city",
            "county",
            "postcode",
            "country",
        ]

        def __init__(self, *args, **kwargs):
            super(WalletForm, self).__init__(*args, **kwargs)
            placeholders = {
                "phone_number": "Phone Number",
                "postcode": "Postcode",
                "town_or_city": "Town or City",
                "street_address1": "Address Line 1",
                "street_address2": "Address Line 2",
                "county": "County",
            }

            for field in self.fields.items():
                if field != "country":
                    if self.fields[field].required:
                        placeholder = f"{placeholders[field]} *"
                    else:
                        placeholder = ""

                self.fields[field].widget.attrs["placeholder"] = placeholder
                self.fields[field].widget.attrs["class"] = "stripe-input"
                self.fields[field].label = False
