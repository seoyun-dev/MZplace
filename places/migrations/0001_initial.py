# Generated by Django 4.2.7 on 2023-11-05 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration_time', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'filters',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=150)),
                ('latitude', models.IntegerField()),
                ('longitude', models.IntegerField()),
                ('work_time', models.CharField(blank=True, max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=100)),
                ('image_url', models.URLField()),
                ('page_url', models.URLField(blank=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.category')),
            ],
            options={
                'db_table': 'places',
            },
        ),
        migrations.CreateModel(
            name='FillterPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.filter')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
            ],
            options={
                'db_table': 'filters_places',
            },
        ),
        migrations.CreateModel(
            name='CoursePlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.course')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
            ],
            options={
                'db_table': 'course_places',
            },
        ),
    ]