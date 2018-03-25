from django.shortcuts import render
from django.http import HttpResponse

from .models import *
# Create your views here.
def index(request):
    ppx = Member.objects.all()[0]
    if ppx.portrait:
      return HttpResponse('Hello, PPX! You look good~~~<br/><img height=240 width=180 src="../' + ppx.portrait.url +'">')
    else:
      return HttpResponse('Hello, PPX! You look good~~~')