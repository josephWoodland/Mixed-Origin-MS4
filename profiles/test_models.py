from django.test import TestCase
from .models import Profile, Wallet
import uuid


def is_valid_uuid(id):
    try:
        uuid.UUID(str(id))
        return True
    except ValueError:
        return False


class ProfileModelTest(TestCase):
    def setUp(self):
        self.profile = Profile()
        self.profile.first_name = "Test"
        self.profile.second_name = "TestSecond"
        self.profile.save()

    def test_fields(self):
        profiles = Profile.objects.all()
        record = profiles[0]
        self.assertEqual(record, self.profile)

    def test_partner_application_is_false(self):
        is_partner = self.profile.is_partner
        self.assertFalse(is_partner)

    def test_is_profile_id_valid_uuid(self):
        id = self.profile.id
        is_true = is_valid_uuid(id)
        self.assertTrue(is_true)

    def test_if_Wallet(self):
        id = self.profile.id
        has_wallet = False
        wallet = Wallet.objects.get(owner=self.profile)
        if wallet:
            has_wallet = True

        self.assertTrue(has_wallet)
