# Generated by Django 3.2 on 2021-04-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='extra_cost',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
