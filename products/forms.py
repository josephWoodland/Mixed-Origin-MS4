from django.forms import ModelForm
from django import forms

from .models import Product


class ProductForm(ModelForm):
    """
    Form for the Product model to allow user input to create instance
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "tags",
            "stock_numbers",
            "price",
            "image",
        ]

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, fields in self.fields.items():
            names = name.capitalize()
            fields.widget.attrs.update({"class": "input", "placeholder": names})
