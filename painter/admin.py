from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from painter.models import Image, Story, User


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ["image"]


admin.site.register(Image, ImageAdmin)


class StoryAdmin(admin.ModelAdmin):
    list_display = ["title", "started", "closed", "activestorycontestmodel"]


admin.site.register(Story, StoryAdmin)


admin.site.register(User, UserAdmin)
