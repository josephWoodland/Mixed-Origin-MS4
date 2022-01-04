# Generated by Django 4.0 on 2021-12-31 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0006_remove_partnerprofile_username"),
        ("products", "0004_tag_product_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profiles.partnerprofile",
            ),
        ),
    ]
