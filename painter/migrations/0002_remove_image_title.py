# Generated by Django 5.0 on 2023-12-09 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('painter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
    ]