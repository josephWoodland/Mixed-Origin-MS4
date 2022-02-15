from django.test import TestCase
from django.urls import reverse, resolve, reverse_lazy
from django.contrib.auth.models import User

from .views import *
from profiles.models import PartnerProfile, Profile
from .models import Product, Tag


class TestProductUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "username", "emal@test.com", "password")
        self.client.login(username="username", password="password")
        self.profile = Profile.objects.get(user=self.user)

        # Create profile object
        self.profile.first_name = "First"
        self.profile.second_name = ("Second",)
        self.profile.username = (self.user.username,)
        self.profile.email = (self.user.email,)
        self.is_partner = True
        self.profile.save()
        self.id = self.profile.id

        # Create Partner object
        self.partner = PartnerProfile.objects.create(
            partner=self.profile, company_name="Test Shop"
        )

        # create tag instances Tag.objects.create()
        self.tag_1 = Tag.objects.create(
            name="Tag 1",
        )
        tag_2 = Tag.objects.create(
            name="Tag 2",
        )
        tag_3 = Tag.objects.create(
            name="Tag 3",
        )

        # Create Product object
        self.product = Product.objects.create(
            owner=self.partner,
            name="Test Product",
        )

        self.products = Product.objects.all()

        # Add the tag to the product
        self.product.tags.add(self.tag_1)
        # .add tags to the product

    def test_products_url_resolves(self):
        url = reverse("products")
        self.assertEquals(resolve(url).func, products)

    def test_products_tags_resolves(self):
        url = reverse("product_tags", kwargs={"tag": self.tag_1.name})
        self.assertEquals(resolve(url).func, product_tags)
