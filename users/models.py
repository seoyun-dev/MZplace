from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id          = models.BigIntegerField(blank=True, null=True)
    naver_id          = models.CharField(blank=True, null=True, max_length=200)
    nickname          = models.CharField(max_length=20)
    user_id           = models.CharField(max_length=50, blank=True)
    password          = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'users'
