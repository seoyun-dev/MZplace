# Generated by Django 4.2.6 on 2024-05-03 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='page_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]