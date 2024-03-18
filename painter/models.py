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

    def winner(self, winning_image):
        locker_contest = LockedStoryContestModel(
            story=self.story,
            winning_image=winning_image.image,
            winning_votes_count=StoryContestImageModelVote.objects.filter(
                image=winning_image
            ).count(),
            close_votes_count=CloseStoryContestModelVote.objects.filter(
                contest=self
            ).count(),
        )
        locker_contest.save()
        for image in StoryContestImageModel.objects.filter(story_contest=self):
            if image != winning_image:
                LockedStoryContestImageModel(
                    story_contest=locker_contest,
                    image=image.image,
                    votes_count=StoryContestImageModelVote.objects.filter(
                        image=image
                    ).count(),
                ).save()
            image.delete()


class LockedStoryContestModel(models.Model):
    story: models.ForeignKey = models.ForeignKey(Story, on_delete=models.CASCADE)
    winning_image: models.ForeignKey = models.ForeignKey(
        Image, on_delete=models.RESTRICT
    )
    close_votes_count: models.IntegerField = models.IntegerField()
    winning_votes_count: models.IntegerField = models.IntegerField()
    time: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["time"]  # or ['-time'] according to the ordering you require


class LockedStoryContestImageModel(models.Model):
    story_contest: models.ForeignKey = models.ForeignKey(
        LockedStoryContestModel, on_delete=models.CASCADE
    )
    votes_count: models.IntegerField = models.IntegerField()
    image: models.ForeignKey = models.ForeignKey(Image, on_delete=models.RESTRICT)


class StoryContestImageModel(models.Model):
    story_contest: models.ForeignKey = models.ForeignKey(
        ActiveStoryContestModel, on_delete=models.CASCADE
    )
    image: models.ForeignKey = models.ForeignKey(Image, on_delete=models.RESTRICT)


class StoryContestImageModelVote(models.Model):
    # user
    image: models.ForeignKey = models.ForeignKey(
        StoryContestImageModel, on_delete=models.CASCADE
    )


class CloseStoryContestModelVote(models.Model):
    contest: models.ForeignKey = models.ForeignKey(
        ActiveStoryContestModel, on_delete=models.CASCADE
    )
