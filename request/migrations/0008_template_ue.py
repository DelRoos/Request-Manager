# Generated by Django 4.0.4 on 2022-07-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0007_template_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='ue',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]