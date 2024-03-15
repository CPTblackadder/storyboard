import base64
import json

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.list import ListView

from .models import (
    ActiveStoryContestModel,
    Image,
    LockedStoryContestImageModel,
    LockedStoryContestModel,
    Story,
    StoryContestImageModel,
)

# Create your views here.


def create_story_painter(request):
    return render(request, "painter/painter.html", {"create_story": True})


def create_image_painter(request, story_id):
    return render(request, "painter/painter.html", {"story_id": story_id})


def submit_new_story(request):
    print("Submitting new story")
    if request.method == "POST":
        try:
            photo = request.POST["canvasData"]
            if "image_text" in request.POST:
                image_text = request.POST["image_text"]
            else:
                image_text = ""
            story_title = request.POST["story_title"]
            print(story_title)
            print(len(story_title))
            if len(story_title) <= 0:
                raise Exception("Must have a story title")
            img_format, img_str = photo.split(";base64,")
            ext = img_format.split("/")[-1]
            img_data = ContentFile(base64.b64decode(img_str), name="temp." + ext)
            # Create and save image
            image = Image.objects.create()
            print("Saving file " + "image_" + str(image.pk) + ".png")
            image.image.save("image_" + str(image.pk) + ".png", img_data)
            image.text = image_text
            image.save()
            story = Story.objects.create()
            story.title = story_title
            story.save()
            first_image_contest = LockedStoryContestModel(
                story=story, winning_image=image
            )
            contest = ActiveStoryContestModel(
                story=story
            )
            contest.save()
            first_image_contest.save()
            return redirect(view_story, story_id=story.pk)
        except Exception as err:
            print("Error: " + str(err))
            # TODO improve failure case
            return render(
                request,
                "painter/painter.html",
                {"submit_error": str(err), "create_story": True},
            )
    return render(request, "painter/painter.html", {"create_story": True})


def submit_new_image(request, story_id):
    print("Submitting new image to story")
    story_contest = get_object_or_404(ActiveStoryContestModel, pk=story_id)
    if request.method == "POST":
        try:
            photo = request.POST["canvasData"]
            if "image_text" in request.POST:
                image_text = request.POST["image_text"]
            else:
                image_text = ""
            img_format, img_str = photo.split(";base64,")
            ext = img_format.split("/")[-1]
            img_data = ContentFile(base64.b64decode(img_str), name="temp." + ext)
            # Create and save image
            image = Image.objects.create()
            print("Saving file " + "image_" + str(image.pk) + ".png")
            image.image.save("image_" + str(image.pk) + ".png", img_data)
            image.text = image_text
            image.save()
            contest_image = StoryContestImageModel(
                story_contest=story_contest, image=image
            )
            contest_image.save()
            return redirect(view_contest, story_id)
        except Exception as err:
            print("Error: " + str(err))
            # TODO improve failure case
            return render(request, "painter/painter.html", {"submit_error": str(err)})
    return render(request, "painter/painter.html")


def view_all(request):
    data = Image.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all_images.html", context)


def view_stories(request):
    data = Story.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all_stories.html", context)


def view_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    locked_images = Image.objects.filter(lockedstorycontestmodel__story__pk=story_id)
    return render(
        request,
        "painter/view_story.html",
        {"story": story, "locked_images": locked_images},
    )


def main(request):
    data = Story.objects.all()
    context = {"data": data}
    return render(request, "painter/landingpage.html", context)


def view_contest(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    contest = get_object_or_404(ActiveStoryContestModel, story=story)
    locked_images = Image.objects.filter(storycontestimagemodel__story_contest=contest)
    return render(
        request,
        "painter/view_contest.html",
        {"story": story, "contest": contest, "locked_images": locked_images},
    )
