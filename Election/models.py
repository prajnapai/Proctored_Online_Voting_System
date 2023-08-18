from django.db import models

# Create your models here.


class Election (models.Model):
    eid = models.IntegerField(primary_key=True, default=None, null=False)
    election_title = models.CharField(max_length=50)
    election_date = models.DateField()
    election_description = models.TextField()
    election_status = models.TextField()
