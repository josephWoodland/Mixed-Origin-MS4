# Generated by Django 4.0 on 2022-01-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0002_alter_order_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="client_secret",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]