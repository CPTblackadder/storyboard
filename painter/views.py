from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

# Create your views here.


def painter(request):
    return render(request, "painter/index.html", {})
