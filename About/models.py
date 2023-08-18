from django.db import models

# Create your models here.

class About (models.Model):
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="about/")
    description = models.TextField()