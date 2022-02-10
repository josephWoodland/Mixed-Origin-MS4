from click import UUID
from django.test import TestCase
from .models import Profile, Wallet
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from .views import *
import uuid
# Create your tests here.


class TestProfileViews(TestCase):

    def setUp(self):
        self.login_url = "/accounts/login/"
        self.user = User.objects.create_user(
            'username', 'emal@test.com', 'password')
        self.client.login(username='username', password='password')

        self.profile = Profile.objects.get(user=self.user)

        self.profile.first_name = "First"
        self.profile.second_name = "Second",
        self.profile.username = self.user.username,
        self.profile.email = self.user.email,
        self.profile.save()

    def test_login_user(self):
        self.assertTrue(self.user.is_authenticated)
