# Generated by Django 4.2.6 on 2024-05-03 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0012_alter_place_page_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
