# Generated by Django 3.0.4 on 2020-03-13 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('RC', models.CharField(max_length=50)),
                ('tel', models.CharField(max_length=50)),
                ('fax', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
