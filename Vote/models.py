from django.db import models

from Candidate.models import Candidate
from Voter.models import Voter
from Election.models import Election

# Create your models here.


class Vote(models.Model):
    vid = models.ForeignKey(Voter, on_delete=models.CASCADE)
    eid = models.ForeignKey(Election, on_delete=models.CASCADE)
    cid = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    casted = models.BooleanField(default=False)


