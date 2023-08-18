from django.db import models

# Create your models here.


class Gallery (models.Model):
    img_title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="gallery/", null=True, default=None)
