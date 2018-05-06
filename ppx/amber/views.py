from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ContactForm

import sys

# Member ================================================================================
class MemberListView(LoginRequiredMixin, ListView):
  model = Member

  def get_context_data(self, **kwargs):
    context = super(MemberListView, self).get_context_data(**kwargs)
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
    context['can_edit_member'] = self.request.user.has_perm('amber.edit_member')
    context['now'] = timezone.now()
    context['dummy'] = 'testing'
    return context

class MemberDetailView(LoginRequiredMixin, DetailView):
  model = Member
  def get_context_data(self, **kwargs):
    context = super(MemberDetailView, self).get_context_data(**kwargs)
    context['can_edit_member'] = self.request.user.has_perm('amber.edit_member')
    context['now'] = timezone.now()
    return context

class MemberCreateView(PermissionRequiredMixin, CreateView):
  model = Member
  template_name_suffix = '_create_form'
  fields = ['name', 'email', 'mobile', 'phone', 'address', 'gender', 'birthday', 'rank', 'tag', 'portrait']
  permission_required = 'amber.edit_member'

class MemberUpdateView(PermissionRequiredMixin, UpdateView):
  model = Member
  template_name_suffix = '_update_form'
  fields = ['email', 'mobile', 'phone', 'address', 'birthday', 'rank', 'tag', 'accumulates', 'n_purchase_orders', 'n_craft_orders', 'status', 'portrait']
  permission_required = 'amber.edit_member'

# Contact ================================================================================
class ContactView(LoginRequiredMixin, FormView):
  template_name = 'amber/contact.html'
  form_class = ContactForm
  success_url = '/amber/'

  def form_valid(self, form):
    form.send_email()
    return super().form_valid(form)

# Store ==================================================================================
class StoreListView(LoginRequiredMixin, ListView):
  model = Store

  def get_context_data(self, **kwargs):
    context = super(StoreListView, self).get_context_data(**kwargs)
    
    context['ylist'] = list(set([ x.inb.date.year for x in context['object_list']]))
    ol = context['object_list']
    date__year = self.request.GET.get('date__year')
    order_by = self.request.GET.get('o')
    context['get_str'] = ''
    if (date__year):
      ol = [ x for x in ol if x.inb.date.year == int(date__year) ]
      context['get_str'] += ('&date__year=' + date__year)
    if (order_by):
      order_by = int(order_by)
      order = abs(order_by)
      if (order == 1):
        ol = sorted(ol, key=lambda i: i.id)
      elif (order == 2):
        ol = sorted(ol, key=lambda i: i.inb.name)
      elif (order == 3):
        ol = sorted(ol, key=lambda i: i.inb.kind)
      elif (order == 4):
        ol = sorted(ol, key=lambda i: i.inb.type)
      elif (order == 5):
        ol = sorted(ol, key=lambda i: i.remains)
      elif (order == 6):
        ol = sorted(ol, key=lambda i: i.inb.unit)
      elif (order == 7):
        ol = sorted(ol, key=lambda i: i.inb.baseprice)
      elif (order == 8):
        ol = sorted(ol, key=lambda i: i.inb.saleprice)
      elif (order == 9):
        ol = sorted(ol, key=lambda i: i.inb.date)
      if (order_by < 0):
        ol.reverse()
      context['order_by'] = order_by
    context['object_list'] = ol
    context['can_in'] = self.request.user.has_perm('amber.canin')
    context['can_viewbase'] = self.request.user.has_perm('amber.viewbase')
    context['now'] = timezone.now()
    context['dummy'] = 'testing'
    return context

class InBoundCreateView(PermissionRequiredMixin, CreateView):
  model = InBound
  template_name_suffix = '_create_form'
  fields = ['name', 'kind', 'type', 'quantity', 'unit', 'baseprice', 'saleprice', 'tag']
  permission_required = 'amber.canin'

  def form_valid(self, form):
    obj = form.save(commit = False)
    obj.save()
    Store(inb=obj, remains=obj.quantity).save()
    return super(InBoundCreateView, self).form_valid(form)

# Create your views here.
@login_required()
def index(request):
  context = {}
  context['now'] = timezone.now()
  group = 'none'
  if (len(request.user.groups.all()) > 0):
    group = str(request.user.groups.all()[0]).lower()
  context['is_group_finance']  = group == 'finance'
  context['is_group_designer'] = group == 'designer'
  context['is_group_sales']    = group == 'sales'
  context['dummy'] = 'testing'
  return render(request, 'amber/index.html', context)

