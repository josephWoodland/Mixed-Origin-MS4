from django.db import models
import uuid
from profiles.models import Profile

# Create your models here.


class Product(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=15)
    description = models.TextField(null=False, blank=False)
    in_stock = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag", blank=True)
    stock_numbers = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

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
