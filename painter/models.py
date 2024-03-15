from django.db import models


class Story(models.Model):
    title: models.CharField = models.CharField(max_length=100)


class Image(models.Model):
    image: models.ImageField = models.ImageField(upload_to="pics")
    text: models.CharField = models.CharField(max_length=128)


# Story has 0..n fixed story parts, which is the image that won the vote, and also all the other images, along with their votes.

# There's a currently open vote or the story is finished
# Open votes have a selection of Images and how many votes there are for them


class ActiveStoryContestModel(models.Model):
    story: models.OneToOneField = models.OneToOneField(
        Story,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class LockedStoryContestModel(models.Model):
    story: models.ForeignKey = models.ForeignKey(Story, on_delete=models.CASCADE)
    winning_image: models.ForeignKey = models.ForeignKey(
        Image, on_delete=models.CASCADE
    )
    time: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["time"]  # or ['-time'] according to the ordering you require


class LockedStoryContestImageModel(models.Model):
    story_contest: models.ForeignKey = models.ForeignKey(
        LockedStoryContestModel, on_delete=models.DO_NOTHING
    )
    image: models.ForeignKey = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    votes: models.IntegerField = models.IntegerField(name="votes")

    class Meta:
        ordering = ["votes"]


class StoryContestImageModel(models.Model):
    story_contest: models.ForeignKey = models.ForeignKey(
        ActiveStoryContestModel, on_delete=models.DO_NOTHING
    )
    image: models.ForeignKey = models.ForeignKey(Image, on_delete=models.DO_NOTHING)


class StoryContestImageModelVote(models.Model):
    # user
    image: models.ForeignKey = models.ForeignKey(
        StoryContestImageModel, on_delete=models.DO_NOTHING
    )
