from django.test import TestCase
from .forms import *


class TestProfileForm(TestCase):

    def test_name_is_required(self):
        form = ProfileForm({"first_name": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors.keys())
        self.assertEqual(form.errors["first_name"]
                         [0], "This field is required.")
