from django.test import TestCase
from profiles.models import PartnerProfile


class ProfileModelTest(TestCase):
    def test_fields(self):
        profile = PartnerProfile()
        profile.company_name = "Test Company Name"
        profile.company_description = (
            "This is a test to see if the description field will be filled out"
        )
        profile.company_short_bio = (
            "his is a test to see if the short bio field will be filled out"
        )
        profile.save()
        profiles = PartnerProfile.objects.all()
        record = profiles[0]
        self.assertEqual(record, profile)
