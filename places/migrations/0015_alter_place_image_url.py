# Generated by Django 4.2.6 on 2024-05-03 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0014_alter_place_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image_url',
            field=models.URLField(max_length=500),
        ),
    ]
