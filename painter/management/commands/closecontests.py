from django.core.management.base import BaseCommand, CommandError

from painter.models import ActiveStoryContestModel, Story


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        for poll_id in options["poll_ids"]:
            try:
                poll = Story.objects.get(pk=poll_id)
            except Story.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
            )
