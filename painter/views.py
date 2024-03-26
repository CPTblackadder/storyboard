import base64
import json

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.list import ListView

from painter.management.commands.closecontests import close_image_contest

from .models import (
    ActiveStoryContestModel,
    CloseStoryContestModelVote,
    Image,
    LockedStoryContestImageModel,
    LockedStoryContestModel,
    Story,
    StoryContestImageModel,
    StoryContestImageModelVote,
)

# Create your views here.


@login_required
def create_story_painter(request):
    return render(request, "painter/painter.html", {"create_story": True})


@login_required
def create_image_painter(request, story_id):
    previous_image = (
        LockedStoryContestModel.objects.filter(story__pk=story_id)
        .order_by("-id")[0]
        .winning_image
    )

    return render(
        request,
        "painter/painter.html",
        {"story_id": story_id, "previous_image": previous_image},
    )


@login_required
def submit_new_story(request):
    print("This must be happening")
    if request.method == "POST":
        try:
            photo = request.POST["canvasData"]
            if "image_text" in request.POST:
                image_text = request.POST["image_text"]
            else:
                image_text = ""
            story_title = request.POST["story_title"]
            if len(story_title) <= 0:
                raise Exception("Must have a story title")
            print("I know this happens")
            img_format, img_str = photo.split(";base64,")
            ext = img_format.split("/")[-1]
            img_data = ContentFile(base64.b64decode(img_str), name="temp." + ext)
            # Create and save image
            image = Image(created_by=request.user, text=image_text)
            image.image.save("image_" + str(image.pk) + ".png", img_data)
            story = Story(title=story_title)
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
            return render(
                request,
                "painter/painter.html",
                {"submit_error": str(err), "create_story": True},
            )
    return render(request, "painter/painter.html", {"create_story": True})


@login_required
def submit_new_image(request, story_id):
    print("Submitting new image")
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
            image = Image(created_by=request.user, text=image_text)
            print("Saving file " + "image_" + str(image.pk) + ".png")
            image.image.save("image_" + str(image.pk) + ".png", img_data)
            contest_image = StoryContestImageModel(
                story_contest=story_contest, image=image
            )
            image.save()
            contest_image.save()
            return redirect(view_story, story_id)
        except Exception as err:
            print("Error: " + str(err))
            # TODO improve failure case
            return render(request, "painter/painter.html", {"submit_error": str(err)})
    return render(request, "painter/painter.html")


@login_required
def view_stories(request):
    data = Story.objects.all()
    context = {"data": data}
    return render(request, "painter/view_all_stories.html", context)


@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    story_images = Image.objects.filter(lockedstorycontestmodel__story__pk=story_id)
    contest = ActiveStoryContestModel.objects.filter(story=story)
    data = {
        "story": story,
        "story_images": story_images,
    }
    if len(contest) == 1:
        data.update(get_contest_data(contest[0]))

    return render(
        request,
        "painter/view_story.html",
        data,
    )


@login_required
def vote_for_image(request, story_id, image_id):
    if request.method == "POST":
        image = get_object_or_404(StoryContestImageModel, pk=image_id)
        image_votes = StoryContestImageModelVote.objects.filter(
            voter=request.user, image__story_contest__story__pk=story_id
        )
        if image_votes.count() < 1:
            # Check for close image contest votes
            close_votes = CloseStoryContestModelVote.objects.filter(
                voter=request.user, contest__story__pk=story_id
            )
            if close_votes.count() >= 1:
                close_votes[0].delete()
            StoryContestImageModelVote(voter=request.user, image=image).save()
        else:
            image_votes[0].delete()
            StoryContestImageModelVote(voter=request.user, image=image).save()
    return redirect(view_story, story_id)


@login_required
def vote_to_finish_story(request, story_id):
    if request.method == "POST":
        contest = get_object_or_404(ActiveStoryContestModel, pk=story_id)
        close_votes = CloseStoryContestModelVote.objects.filter(
            voter=request.user, contest__story__pk=story_id
        )
        if close_votes.count() == 0:
            image_votes = StoryContestImageModelVote.objects.filter(
                voter=request.user, image__story_contest__story__pk=story_id
            )
            if image_votes.count() >= 1:
                image_votes[0].delete()
            CloseStoryContestModelVote(voter=request.user, contest=contest).save()
    return redirect(view_story, story_id)

@login_required
def view_image(request, story_id, image_id):
    story = get_object_or_404(Story, pk=story_id)
    image = get_object_or_404(StoryContestImageModel, pk=image_id)
    return render(
        request,
        "painter/view_image.html",
        {"story": story, "image": image},
    )


@login_required
def main(request):
    open_stories = Story.objects.filter(activestorycontestmodel__isnull=False).order_by(
        "-started"
    )[:3]
    closed_stories = Story.objects.filter(
        activestorycontestmodel__isnull=True
    ).order_by("-closed")[:3]
    for story in open_stories:
        images = LockedStoryContestModel.objects.filter(story=story).order_by("-id")
        story.number_of_images = len(images)
        story.more_than_five_images = story.number_of_images > 5
        story.images = reversed(images[:5])
    for story in closed_stories:
        images = LockedStoryContestModel.objects.filter(story=story).order_by("-id")
        story.number_of_images = len(images)
        story.more_than_five_images = story.number_of_images > 5
        story.images = reversed(images[:5])

    context = {"open_stories": open_stories, "closed_stories": closed_stories}
    return render(request, "painter/landingpage.html", context)


def get_contest_data(contest):
    votes_to_close_contest = CloseStoryContestModelVote.objects.filter(
        contest=contest
    ).count()
    images = (
        StoryContestImageModel.objects.filter(story_contest=contest)
        .annotate(votes=Count("storycontestimagemodelvote"))
        .order_by("-votes")
    )
    return {
        "contest": contest,
        "contest_images": images,
        "votes_to_close_contest": votes_to_close_contest,
    }


@login_required
def close_contest(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    contest = get_object_or_404(ActiveStoryContestModel, story=story)
    close_image_contest(contest)
    return redirect(view_story, story_id)
