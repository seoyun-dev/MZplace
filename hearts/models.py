from django.db     import models

from core.models   import TimeStampModel
from users.models  import User
from places.models import Place, Course

class Heart(TimeStampModel):
    place   = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    course  = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hearts'