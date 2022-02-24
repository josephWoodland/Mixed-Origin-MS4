from django.db import models
import uuid
from mixed.settings import MEDIA_ROOT, MEDIA_URL
from profiles.models import PartnerProfile
from PIL import Image
import os


# Create your models here.


class Product(models.Model):
    """
    Product model that creates an instance of the Product Class
    """

    owner = models.ForeignKey(
        PartnerProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=False)
    in_stock = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag", blank=True)
    stock_numbers = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(
        default=0, decimal_places=2, max_digits=7, null=False, blank=False
    )

    image = models.ImageField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    slug = models.CharField(max_length=200, null=True, unique=True)

    def save(self, *args, **kwargs):

        # super().save(*args, **kwargs)

        if self.image:

            image = Image.open(self.image)
            image = image.convert("RGB")
            name = str(self.image) + ".webp"

            if "USE_AWS" in os.environ:
                media_folder = MEDIA_URL
                image.save(f"{media_folder}{name}", "webp")
            else:
                media_folder = MEDIA_ROOT
                image.save(f"{media_folder}/{name}", "webp")

            self.image = name

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
