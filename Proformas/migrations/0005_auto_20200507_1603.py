# Generated by Django 3.0.4 on 2020-05-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proformas', '0004_commande_date_validation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='Date_validation',
            field=models.DateField(),
        ),
    ]
