# Generated by Django 4.0 on 2022-01-31 12:52

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0004_rename_client_secret_order_stripe_pid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="country",
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
