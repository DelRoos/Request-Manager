# Generated by Django 4.0.4 on 2022-07-13 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_alter_template_status_requestimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='commentaire',
        ),
    ]