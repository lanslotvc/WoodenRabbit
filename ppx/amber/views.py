from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView


from .models import *
from .forms import ContactForm

# Member ================================================================================
class MemberListView(ListView):
  model = Member

  def get_context_data(self, **kwargs):
    context = super(MemberListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

class MemberDetailView(DetailView):
  model = Member
  def get_context_data(self, **kwargs):
    context = super(MemberDetailView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

class MemberCreateView(CreateView):
  model = Member
  template_name_suffix = '_create_form'
  fields = ['name', 'email', 'mobile', 'phone', 'address', 'gender', 'birthday', 'rank', 'tag', 'portrait']

# Contact ================================================================================
class ContactView(FormView):
  template_name = 'amber/contact.html'
  form_class = ContactForm
  success_url = '/amber/'

  def form_valid(self, form):
    form.send_email()
    return super().form_valid(form)


# Create your views here.
def index(request):
  return render(request, 'amber/index.html', None)


def porders(request):
  return HttpResponse('porders')

def porder(request):
  return HttpResponse('porder')

def corders(request):
  return HttpResponse('corders')

def corder(request):
  return HttpResponse('corder')
