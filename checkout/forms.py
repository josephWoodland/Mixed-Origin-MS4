from django import forms
from checkout.models import Order


class OrderForm(forms.ModelForm):
    class Meta:

        model = Order

        fields = (
            "full_name",
            "email",
            "phone_number",
            "country",
            "postcode",
            "town_or_city",
            "street_address1",
            "street_address2",
            "county",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "postcode": "Postcode",
            "town_or_city": "Town or City",
            "street_address1": "Address Line 1",
            "street_address2": "Address Line 2",
            "county": "County",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field != "country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]

            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-input"
            self.fields[field].label = False
