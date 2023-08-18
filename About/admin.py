from django.contrib import admin
from About.models import About

# Register your models here.


class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'description')


admin.site.register(About, AboutAdmin)

