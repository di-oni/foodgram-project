# Generated by Django 2.2.19 on 2021-08-18 07:00

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20210818_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.DecimalField(decimal_places=1, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.1000000000000000055511151231257827021181583404541015625'))], verbose_name='Количество'),
        ),
    ]
