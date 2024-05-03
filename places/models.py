from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'


class Place(models.Model):
    name         = models.CharField(max_length=100)
    district     = models.CharField(max_length=100)
    address      = models.CharField(max_length=150)
    latitude     = models.DecimalField(max_digits=11, decimal_places=8)
    longitude    = models.DecimalField(max_digits=11, decimal_places=8)
    work_time    = models.CharField(max_length=200, blank=True)
    price        = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, blank=True)
    image_url    = models.URLField(max_length=400)
    page_url     = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    category     = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'places'


class Filter(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'filters'


class FilterPlace(models.Model):
    filter = models.ForeignKey('Filter', on_delete=models.CASCADE)
    place  = models.ForeignKey('Place', on_delete=models.CASCADE)

    class Meta:
        db_table = 'filters_places'


class Course(models.Model):
    name          = models.CharField(max_length=100)
    duration_time = models.CharField(max_length=100)
    price         = models.CharField(max_length=100)
    image_url     = models.CharField(max_length=400)

    class Meta:
        db_table = 'courses'


class CoursePlace(models.Model):
    course       = models.ForeignKey('Course', on_delete=models.CASCADE)
    place        = models.ForeignKey('Place', on_delete=models.CASCADE)
    order_number = models.IntegerField()

    class Meta:
        db_table = 'course_places'