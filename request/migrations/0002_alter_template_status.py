# Generated by Django 4.0.4 on 2022-06-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='status',
            field=models.CharField(choices=[('En redaction', 'En redaction'), ('En attente', 'En attente'), ('En traitement', 'En traitement'), ('Terminer', 'Terminer')], default='En redaction', max_length=15),
        ),
    ]