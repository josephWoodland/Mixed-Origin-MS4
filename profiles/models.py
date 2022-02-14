from django.db import models
from django.contrib.auth.models import User
import uuid

from django_countries.fields import CountryField

# Create your models here.


class Profile(models.Model):
    """
    Profile model used to create an instance of the Profile class
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    second_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(
        null=False,
        blank=False,
        upload_to="profiles/",
    )
    partner_application = models.BooleanField(
        default=False, blank=True, null=True)
    application_email_sent = models.BooleanField(
        default=False, blank=True, null=True)
    is_partner = models.BooleanField(
        default=False, blank=True, null=True)
    partner_email_sent = models.BooleanField(
        default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.username)


class PartnerProfile(models.Model):
    """
    Partner Profile Model used to create instance of the PartnerProfile class
    """

    partner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    company_image = models.ImageField(
        null=False,
        blank=False,
        default="default.png",
        upload_to="companies/",
    )
    company_name = models.CharField(max_length=50, blank=False, null=False)
    company_website = models.CharField(max_length=200, null=True, blank=False)
    company_short_bio = models.TextField(
        max_length=200, null=False, blank=False)
    company_description = models.TextField(
        max_length=400, null=False, blank=False)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    promoted = models.BooleanField(default=False, blank=True, null=True)

    slug = models.CharField(max_length=200, null=True, unique=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.company_name)


class Wallet(models.Model):
    """
    Wallet Model used to create an instance of the Wallet Class
    """

    owner = models.OneToOneField(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=200, blank=False, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label="Country", null=True, blank=True)

    def __str__(self):
        return str(self.owner.username)
