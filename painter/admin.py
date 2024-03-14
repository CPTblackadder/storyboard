from django.contrib import admin

from painter.models import Image

# Register your models here.


class imageAdmin(admin.ModelAdmin):
    list_display = ["image"]


admin.site.register(Image, imageAdmin)
