from django.db import models
from django.conf import settings
from profiles.views import Profile
from products.views import Product
from django_countries.fields import CountryField
from django.db.models import Sum

import uuid


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders"
    )
    full_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.IntegerField(null=True, blank=False)
    country = CountryField(blank_label="Country *", null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=False, blank=False)
    county = models.CharField(max_length=40, null=False, blank=False)
    delivery_costs = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    created = models.DateTimeField(auto_now_add=True)
    stripe_pid = models.CharField(max_length=200, null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        ordering = ["-created"]

    def total(self):

        self.sub_total = self.items.aggregate(Sum("item_total"))[
            "item_total__sum"]

        # Fixes a bug when deleting orders from the Admin
        if self.sub_total is None:
            # If the sub_total has been deleted and now None return
            return self

        if self.sub_total < settings.FREE_STANDARD_DELIVERY_THRESHOLD:
            self.delivery_costs = settings.STANDARD_DELIVERY_CHARGE
        else:
            self.delivery_costs = 0

        self.grand_total = self.sub_total + self.delivery_costs
        self.save()

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, null=False, blank=True, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, null=False, blank=True, on_delete=models.CASCADE
    )

    quantity = models.IntegerField(null=False, blank=False, default=0)

    item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0, editable=False
    )
    # ad a space for the product owner

    def total(self, *args, **kwargs):
        self.item_total = int(self.product.price * self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f"ID { self.product.id } : { self.product.name }")
