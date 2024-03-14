from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="landingpage"),
    path("painter", views.painter, name="painter"),
    path("view", views.view_all, name="viewer"),
    path("submit", views.submit, name="submit"),
    path("stories", views.view_stories, name="stories"),
]
