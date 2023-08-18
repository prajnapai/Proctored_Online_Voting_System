from django.contrib import admin
from Candidate.models import Candidate

# Register your models here.


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('cid', 'can_name', 'age', 'gender', 'party', 'symbol')


admin.site.register(Candidate, CandidateAdmin)

# Register your models here.
