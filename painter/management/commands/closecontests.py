import datetime
from operator import attrgetter

from django.core.management.base import BaseCommand, CommandError

from painter.models import (
    ActiveStoryContestModel,
    CloseStoryContestModelVote,
    Story,
    StoryContestImageModel,
    StoryContestImageModelVote,
)


class Command(BaseCommand):
    help = "Closes the all open contests"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for contest in ActiveStoryContestModel.objects.all():
            close_image_contest(contest)


def close_image_contest(contest: ActiveStoryContestModel):
    options = [
        CloseVote(CloseStoryContestModelVote.objects.filter(contest=contest).count())
    ] + [
        NewImage(
            StoryContestImageModelVote.objects.filter(image=image).count(),
            image,
        )
        for image in StoryContestImageModel.objects.filter(story_contest=contest)
    ]
    most_votes = max(options, key=attrgetter("votes"))
    options = [i for i in options if i.votes == most_votes.votes]
    if len(options) != 1:
        pass
    else:
        # Now we can do the action
        options[0].do_action(contest)
        pass


class NewImage:
    def __init__(self, votes, image) -> None:
        self.votes = votes
        self.image: StoryContestImageModel = image

    def do_action(self, contest: ActiveStoryContestModel):
        contest.winner(self.image)


class CloseVote:
    def __init__(self, votes) -> None:
        self.votes = votes

    def do_action(self, contest: ActiveStoryContestModel):
        # Remove the contest
        contest.story.closed = datetime.datetime.now(datetime.UTC)
        contest.story.save()
        contest.delete()
