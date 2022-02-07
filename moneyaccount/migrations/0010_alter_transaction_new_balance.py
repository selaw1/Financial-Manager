# Generated by Django 4.0.1 on 2022-02-05 17:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneyaccount', '0009_alter_transaction_new_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='new_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
