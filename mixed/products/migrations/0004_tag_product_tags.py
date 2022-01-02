# Generated by Django 4.0 on 2021-12-31 21:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_stock_numbers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='products.Tag'),
        ),
    ]