# Generated by Django 4.2.6 on 2024-05-03 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_alter_place_work_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='phone_number',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
