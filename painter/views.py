import base64
import json

from django.core.files.base import ContentFile
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.list import ListView

from painter.management.commands.closecontests import close_image_contest

from .models import (
    ActiveStoryContestModel,
    Image,
    LockedStoryContestImageModel,
    LockedStoryContestModel,
    Story,
    StoryContestImageModel,
    StoryContestImageModelVote,
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
            story = Story.objects.create()
            story.title = story_title
            first_image_contest = LockedStoryContestModel(
                story=story,
                winning_image=image,
                close_votes_count=0,
                winning_votes_count=0,
            )
            contest = ActiveStoryContestModel(story=story)
            image.save()
            story.save()
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


def view_stories(request):
    data = Story.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all_stories.html", context)


def view_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    story_images = Image.objects.filter(lockedstorycontestmodel__story__pk=story_id)
    contest = ActiveStoryContestModel.objects.filter(story=story)
    data = {
        "story": story,
        "story_images": story_images,
    }
    contest_images = None
    if len(contest) == 1:
        contest_images = StoryContestImageModel.objects.filter(
            story_contest=contest[0]
        ).annotate(votes=Count("storycontestimagemodelvote"))
        data.update(
            {
                "contest": contest,
                "contest_images": contest_images,
            }
        )

    return render(
        request,
        "painter/view_story.html",
        data,
    )


def vote_for_image(request, story_id, image_id):
    # TODO add user auth
    image = get_object_or_404(StoryContestImageModel, pk=image_id)
    StoryContestImageModelVote(image=image).save()
    return redirect(view_contest, story_id)


def view_image(request, story_id, image_id):
    story = get_object_or_404(Story, pk=story_id)
    image = get_object_or_404(StoryContestImageModel, pk=image_id)
    return render(
        request,
        "painter/view_image.html",
        {"story": story, "image": image},
    )


def main(request):
    data = Story.objects.all()
    for story in data:
        images = LockedStoryContestModel.objects.filter(story=story).order_by("-id")
        story.number_of_images = len(images)
        story.more_than_five_images = story.number_of_images > 5
        story.images = reversed(images[:5])
    context = {"data": data}
    return render(request, "painter/landingpage.html", context)


def view_contest(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    contest = get_object_or_404(ActiveStoryContestModel, story=story)

    images = StoryContestImageModel.objects.filter(story_contest=contest).annotate(
        votes=Count("storycontestimagemodelvote")
    )
    return render(
        request,
        "painter/view_contest.html",
        {"story": story, "contest": contest, "contest_images": images},
    )


def close_contest(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    contest = get_object_or_404(ActiveStoryContestModel, story=story)
    close_image_contest(contest)
    return redirect(view_story, story_id)
