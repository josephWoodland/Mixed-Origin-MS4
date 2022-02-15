import profile
from click import UUID
from django.http import response
from django.test import TestCase, Client
from .models import Profile, Wallet
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from .views import *
import uuid

# Create your tests here.


class TestProfileViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "username", "emal@test.com", "password")
        self.client = Client()
        self.client.login(username="username", password="password")

        self.profile = Profile.objects.get(user=self.user)
        self.profile.first_name = "First"
        self.profile.second_name = ("Second",)
        self.profile.username = (self.user.username,)
        self.profile.email = (self.user.email,)
        self.profile.save()
        self.id = self.profile.id
        print("Self id: ", self.id)
        id = self.id

    def test_login_user(self):
        self.assertTrue(self.user.is_authenticated)

    def test_edit_profile(self):
        this_id = self.id
        response = self.client.get(f"/profile/edit-profile/{this_id}")
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "profiles/edit_profile.html")

    # def test_user_profile(self):
    #     response = self.client.get("/")
    #     # print(request.user)
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "profiles/profile.html")

    def test_delete_profile(self, pk=id):
        response = self.client.get(f'/profile/delete-profile/{self.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "includes/delete_template.html")
