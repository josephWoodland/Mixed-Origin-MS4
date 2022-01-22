from django.db import models
from .views import order_number_generator
import uuid
from profiles.views import Profile
from products.views import Product
from django.conf import settings
from django.db.models import Sum

# Create your models here.


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.DO_NOTHING
    )
    order_number = models.CharField(max_length=20, default=order_number_generator)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.IntegerField(null=True, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
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
    tracking_number = models.CharField(max_length=40, null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def tracking_number(self, *args, **kwargs):
        name_id = self.full_name[:2]
        postcode_id = self.postcode[:2]
        order_number = str(self.order_number)
        self.tracking_number = name_id + postcode_id + order_number
        super().save(*args, **kwargs)

    def total(self):
        self.sub_total = self.OrderItem.aggregate(sum("item_total"))["item_total__sum"]
        if self.sub_total < settings.FREE_STANDARD_DELIVERY_THRESHOLD:
            self.delivery_costs = settings.STANDARD_DELIVERY_CHARGE
        else:
            self.delivery_costs = 0

        self.grand_total = self.sub_total + self.delivery_costs
        self.save()

    def __str__(self):
        return self.tracking_number


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

    def total(self, *args, **kwargs):
        self.item_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID { self.product.id } in order { self.tracking_number }"
