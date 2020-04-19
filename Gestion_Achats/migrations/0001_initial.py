# Generated by Django 3.0.4 on 2020-04-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(max_length=200)),
                ('Code', models.CharField(max_length=200)),
                ('Description', models.CharField(max_length=200)),
                ('Service', models.BooleanField()),
            ],
        ),
    ]
