# Generated by Django 4.2.6 on 2024-05-03 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0010_alter_place_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='place',
            name='page_url',
            field=models.URLField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='place',
            name='phone_number',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
