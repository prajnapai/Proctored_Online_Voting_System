from django.contrib import admin
from Voter.models import Voter

# Register your models here.


class VoterAdmin(admin.ModelAdmin):
    list_display = ('vid', 'name', 'photo', 'age', 'gender', 'dob', 'address', 'phone', 'constituency')


admin.site.register(Voter, VoterAdmin)