from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import *
# Create your views here.
def index(request):
  return render(request, 'amber/index.html', None)
      
def members(request):
  members = Member.objects.all()
  return render(request, 'amber/members.html', {'members': members})

def member(request, m_id):
  member = get_object_or_404(Member, pk=m_id)
  return render(request, 'amber/member.html', {'member': member})

def porders(request):
  return HttpResponse('porders')

def porder(request):
  return HttpResponse('porder')

def corders(request):
  return HttpResponse('corders')

def corder(request):
  return HttpResponse('corder')
