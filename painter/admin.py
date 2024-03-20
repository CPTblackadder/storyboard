from django.contrib import admin

from painter.models import Image, Story

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = ["image"]


admin.site.register(Image, ImageAdmin)


class StoryAdmin(admin.ModelAdmin):
    list_display = ["title", "started", "closed"]


admin.site.register(Story, StoryAdmin)
