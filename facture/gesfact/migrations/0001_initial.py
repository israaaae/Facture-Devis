# Generated by Django 4.2.4 on 2023-08-21 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('cout_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email', models.EmailField(max_length=254)),
                ('numero_telephone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_facture', models.CharField(max_length=100)),
                ('date_emission', models.DateField(default=django.utils.timezone.now)),
                ('quantite', models.PositiveIntegerField()),
                ('serie', models.CharField(max_length=100)),
                ('remise', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('montant_paye', models.DecimalField(decimal_places=2, max_digits=10)),
                ('statut', models.CharField(choices=[('paye', 'Payé'), ('partiellement_paye', 'Partiellement payé'), ('impaye', 'Impayé')], default='impaye', max_length=20)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gesfact.article')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gesfact.client')),
            ],
        ),
        migrations.CreateModel(
            name='Devis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_devis', models.CharField(max_length=50)),
                ('client', models.CharField(max_length=20)),
                ('date_emission', models.DateField(default=django.utils.timezone.now)),
                ('quantite', models.PositiveIntegerField()),
                ('serie', models.CharField(max_length=50)),
                ('remise', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='devis/pdfs/')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gesfact.article')),
            ],
        ),
    ]
