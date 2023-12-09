from django.urls import path

from . import views

urlpatterns = [
    path("", views.painter, name="painter"),
    path("view", views.view_all, name="viewer"),
    path("submit", views.submit, name="submit"),
]
