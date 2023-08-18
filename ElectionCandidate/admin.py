from django.contrib import admin
from .models import ElectionCandidate


class ElectionCandidateAdmin(admin.ModelAdmin):
    list_display = ('election', 'candidate')


admin.site.register(ElectionCandidate, ElectionCandidateAdmin)
