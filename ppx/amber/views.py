from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView

from .models import *
from .forms import ContactForm

import sys

# Member ================================================================================
class MemberListView(ListView):
  model = Member

  def get_context_data(self, **kwargs):
    context = super(MemberListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now() #self.request.user#
    context['ylist'] = list(set([ x.join_date.year for x in context['member_list']]))
    ol = context['object_list']
    join_date__year = self.request.GET.get('join_date__year')
    order_by = self.request.GET.get('o')
    context['get_str'] = ''
    if (join_date__year):
      ol = [ x for x in ol if x.join_date.year == int(join_date__year) ]
      context['get_str'] += ('&join_date__year=' + join_date__year)
    if (order_by):
      order_by = int(order_by)
      order = abs(order_by)
      if (order == 1):
        ol = sorted(ol, key=lambda m: m.name)
      elif (order == 2):
        ol = sorted(ol, key=lambda m: m.accumulates)
      elif (order == 3):
        ol = sorted(ol, key=lambda m: m.n_purchase_orders)
      elif (order == 4):
        ol = sorted(ol, key=lambda m: m.n_craft_orders)
      if (order_by < 0):
        ol.reverse()
      context['order_by'] = order_by
    context['object_list'] = ol
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

class MemberUpdateView(UpdateView):
  model = Member
  template_name_suffix = '_update_form'
  fields = ['email', 'mobile', 'phone', 'address', 'rank', 'tag', 'portrait', 'accumulates', 'n_purchase_orders', 'n_craft_orders', 'status']

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
