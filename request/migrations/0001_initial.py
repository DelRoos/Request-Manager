# Generated by Django 4.0.4 on 2022-05-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examen', models.CharField(max_length=10)),
                ('note1', models.CharField(max_length=10)),
                ('note2', models.CharField(max_length=10)),
                ('commentaire', models.TextField()),
            ],
        ),
    ]