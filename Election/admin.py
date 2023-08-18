from django.contrib import admin
from Election.models import Election

# Register your models here.


class ElectionAdmin(admin.ModelAdmin):
    list_display = ('eid', 'election_title', 'election_date', 'election_description', 'election_status')


admin.site.register(Election, ElectionAdmin)