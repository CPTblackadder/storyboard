from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="landingpage"),
    path("create", views.create_story_painter, name="createstory"),
    path("create/submit", views.submit_new_story, name="submitstory"),
    path("story/<int:story_id>", views.view_story, name="viewstory"),
    path(
        "story/<int:story_id>/contest",
        views.view_contest,
        name="viewcontest",
    ),
    path(
        "story/<int:story_id>/create", views.create_image_painter, name="createcontest"
    ),
    path("story/<int:story_id>/submit", views.submit_new_image, name="submitimage"),
    path("view", views.view_all, name="viewer"),
    path("stories", views.view_stories, name="stories"),
]
