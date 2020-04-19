# Generated by Django 3.0.4 on 2020-04-19 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Fournis_Section', '0001_initial'),
        ('Gestion_Achats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(auto_now_add=True)),
                ('Montant_HT', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TVA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Montant_TTC', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Id_Fournis', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Fournis_Section.Fournis_Data')),
            ],
        ),
        migrations.CreateModel(
            name='Assocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Id_Achats', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Gestion_Achats.Achats')),
                ('Id_Article', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Gestion_Achats.Article')),
            ],
        ),
    ]
