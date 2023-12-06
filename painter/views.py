from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def painter(request):
    return HttpResponse("This is where the painting app will go")
