from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import *


class TestProfileUrls(TestCase):
    def setUp(self):
        self.login_url = "/accounts/login/"
        self.user = User.objects.create_user(
            "username", "emal@test.com", "password")
        self.client.login(username="username", password="password")

        self.profile = Profile.objects.get(user=self.user)

        self.profile.first_name = "First"
        self.profile.second_name = ("Second",)
        self.profile.username = (self.user.username,)
        self.profile.email = (self.user.email,)
        self.profile.save()
        self.id = self.profile.id

    def test_profile_url_resolves(self):
        url = reverse("profile")
        self.assertEquals(resolve(url).func, user_profile)

    def test_edit_profile_url_resolves(self):
        url = reverse("edit-profile", kwargs={"pk": self.id})
        self.assertEquals(resolve(url).func, edit_profile)

    def test_edit_partner_url_resolves(self):
        url = reverse("edit-partner", kwargs={"pk": self.id})
        self.assertEquals(resolve(url).func, edit_partner)

    def test_delete_profile_url_resolves(self):
        url = reverse("delete-profile", kwargs={"pk": self.id})
        self.assertEquals(resolve(url).func, delete_profile)

    def test_wallet_url_resolves(self):
        url = reverse("wallet", kwargs={"pk": self.id})
        self.assertEquals(resolve(url).func, user_wallet)

    def test_orders_url_resolves(self):
        url = reverse("orders", kwargs={"pk": self.id})
        self.assertEquals(resolve(url).func, orders)
