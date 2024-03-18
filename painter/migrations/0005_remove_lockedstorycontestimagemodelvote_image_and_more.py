# Generated by Django 5.0 on 2024-03-18 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('painter', '0004_alter_lockedstorycontestimagemodel_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lockedstorycontestimagemodelvote',
            name='image',
        ),
        migrations.AddField(
            model_name='lockedstorycontestimagemodel',
            name='votes_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lockedstorycontestmodel',
            name='close_votes_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lockedstorycontestmodel',
            name='winning_votes_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='LockedCloseStoryContestModelVote',
        ),
        migrations.DeleteModel(
            name='LockedStoryContestImageModelVote',
        ),
    ]