from django.db import models

from Candidate.models import Candidate
from Election.models import Election


# Create your models here.
class ElectionCandidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    # platform = models.TextField()
    # campaign_budget = models.DecimalField(max_digits=10, decimal_places=2)
    # add any other fields you need to store information about the candidate's campaign for this election
