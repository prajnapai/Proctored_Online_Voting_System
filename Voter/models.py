from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Voter (models.Model):
    vid = models.CharField(max_length=10, primary_key=True, default=None, null=False)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="voter/", null=True, default=None)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    address = models.TextField()
    phone = models.IntegerField()
    constituency = models.CharField(max_length=50)

