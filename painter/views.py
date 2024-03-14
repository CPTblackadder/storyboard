import base64
import json

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Story, StoryContestImageModel

# Create your views here.


def painter(request):
    return render(request, "painter/painter.html")


def submit(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            photo = body["photo"]
            img_format, img_str = photo.split(";base64,")
            ext = img_format.split("/")[-1]
            img_data = ContentFile(base64.b64decode(img_str), name="temp." + ext)
            image = StoryContestImageModel.objects.create()
            print("Saving file " + "image_" + str(image.pk) + ".png")
            image.image.save("image_" + str(image.pk) + ".png", img_data)
            # image.story_contest =
            image.save()
            return redirect(view_all)
        except Exception as err:
            print("Error: " + str(err))
            # TODO improve failure case
            return render(request, "painter/painter.html", {"submit_error": str(err)})
    return render(request, "painter/painter.html")


def view_all(request):
    data = StoryContestImageModel.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all_images.html", context)


def view_stories(request):
    data = Story.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all_stories.html", context)


def main(request):
    data = Story.objects.all()
    context = {"data": data}
    return render(request, "painter/landingpage.html", context)
