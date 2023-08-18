from django.db import models


class Candidate (models.Model):
    cid = models.IntegerField(primary_key=True, default=None, null=False)
    can_name = models.CharField(max_length=50)
    can_photo=models.ImageField(upload_to='candidate/', null=True, blank=True)
    age = models.IntegerField()
    gender=models.CharField(max_length=1)
    party=models.CharField(max_length=50)
    symbol=models.ImageField(upload_to='candidate/')