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
        print("Got post")
        body = json.loads(request.body)
        print("Loaded JSON")
        photo = body["photo"]
        img_format, img_str = photo.split(";base64,")
        ext = img_format.split("/")[-1]
        img_data = ContentFile(base64.b64decode(img_str), name="temp." + ext)
        print("Converted Image")
        try:
            print("Making image")
            image = Image.objects.create()
            print("Saving file " + "image_" + str(image.pk) + ".png")
            image.photo.save("image_" + str(image.pk) + ".png", img_data)
            image.save()
            return redirect("viewer")
        except Exception as err:
            print("Error: " + str(err))
            return render(request, "painter/painter.html", { "submit_error": str(err)})
    else:
        return render(request, "painter/painter.html", { "submit_error": "Not a post request"})


def view_all(request):
    data = Image.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all.html", context)
