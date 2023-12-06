from django.urls import path

from . import views

urlpatterns = [
    path("/painter", views.painter, name="painter"),
]
