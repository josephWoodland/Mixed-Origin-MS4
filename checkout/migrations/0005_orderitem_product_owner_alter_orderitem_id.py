# Generated by Django 4.0 on 2022-02-11 10:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0004_alter_order_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="product_owner",
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
