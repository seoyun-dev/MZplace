from django.db import models

from core.models import TimeStampModel
from users.models import User
from places.models import Place, Course


class Review(TimeStampModel):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    place   = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=150)
    rating  = models.IntegerField()

    class Meta:
        db_table = 'reviews'