# Generated by Django 4.0 on 2022-02-09 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_product_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="owner_profile",
        ),
    ]