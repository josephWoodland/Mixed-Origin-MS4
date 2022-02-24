# Generated by Django 4.0 on 2022-02-13 15:40

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0005_product_webp_image"),
        ("profiles", "0010_merge_20220211_1537"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=200)),
                ("phone_number", models.IntegerField(null=True)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("postcode", models.CharField(max_length=20)),
                ("town_or_city", models.CharField(max_length=40)),
                ("street_address1", models.CharField(max_length=80)),
                ("street_address2", models.CharField(max_length=80)),
                ("county", models.CharField(max_length=40)),
                (
                    "delivery_costs",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=6),
                ),
                (
                    "sub_total",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "grand_total",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("stripe_pid", models.CharField(
                    blank=True, max_length=200, null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("quantity", models.IntegerField(default=0)),
                (
                    "item_total",
                    models.DecimalField(
                        decimal_places=2, default=0, editable=False, max_digits=6
                    ),
                ),
                (
                    "product_owner",
                    models.CharField(max_length=200, null=True, unique=True),
                ),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="checkout.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
