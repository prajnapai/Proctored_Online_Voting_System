from django.contrib import admin
from Gallery.models import Gallery

# Register your models here.
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('img_title', 'image')


admin.site.register(Gallery, GalleryAdmin)