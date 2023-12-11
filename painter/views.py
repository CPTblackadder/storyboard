import base64
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.base import ContentFile
from .models import Image

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
            image = Image.objects.create()
            print("Saving file " + "image_" + str(image.pk) + ".png")
            image.photo.save("image_" + str(image.pk) + ".png", img_data)
            image.save()
            return redirect(view_all)
        except Exception as err:
            print("Error: " + str(err))
            # TODO improve failure case
            return render(request, "painter/painter.html", {"submit_error": str(err)})
    return render(request, "painter/painter.html")


def view_all(request):
    data = Image.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all.html", context)
