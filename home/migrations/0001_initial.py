# Generated by Django 4.0.4 on 2022-04-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('describe', models.CharField(max_length=500)),
                ('profile', models.ImageField(upload_to='media/profile')),
            ],
        ),
    ]
