# Generated by Django 4.0 on 2022-01-05 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_alter_wallet_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='account_number',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='phone_number',
        ),
    ]
