# Generated by Django 4.2.6 on 2024-05-03 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_alter_place_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
