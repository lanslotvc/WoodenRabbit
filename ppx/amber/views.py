from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ContactForm

import sys
import types

# Member ================================================================================
class MemberListView(LoginRequiredMixin, ListView):
  model = Member

  def get_context_data(self, **kwargs):
    context = super(MemberListView, self).get_context_data(**kwargs)
    context['ylist'] = list(set([ x.join_date.year for x in context['member_list']]))
    ol = context['object_list']
    join_date__year = self.request.GET.get('join_date__year')
    join_date__year = None if join_date__year == 'C' else join_date__year
    gender = self.request.GET.get('gender')
    gender = None if gender == 'C' else gender
    rank = self.request.GET.get('rank')
    rank = None if rank == 'C' else rank
    status = self.request.GET.get('status')
    status = None if status == 'C' else status
    order_by = self.request.GET.get('o')
    q = self.request.GET.get('q')
    context['get_str'] = ''
    # query
    if (q):
      l = []
      for m in ol:
        if (q in m.name) or (q in m.wechat) or (q in m.email) or (q in str(m.mobile)) or (q in str(m.phone)) or (q in m.address) or (q in str(m.birthday)) or (q in m.tag):
          l.append(m)
      ol = l
      context['q'] = l
    # filter
    if (join_date__year):
      ol = [ x for x in ol if x.join_date.year == int(join_date__year) ]
      context['get_str'] += ('&join_date__year=' + join_date__year)
      context['y'] = int(join_date__year)
    if (gender):
      ol = [ x for x in ol if x.gender == int(gender) ]
      context['get_str'] += ('&gender=' + gender)
      context['g'] = int(gender)
    if (rank):
      ol = [ x for x in ol if x.rank == int(rank) ]
      context['get_str'] += ('&rank=' + rank)
      context['r'] = int(rank)
    if (status):
      ol = [ x for x in ol if x.status == int(status) ]
      context['get_str'] += ('&status=' + status)
      context['s'] = int(status)
    # order
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
      elif (order == 5):
        ol = sorted(ol, key=lambda m: m._next_birth())
      elif (order == 6):
        ol = sorted(ol, key=lambda m: m.ds_acc)
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
    member = context['member']
    if member.upstream:
      ups = Member.objects.filter(mobile=member.upstream)
      if len(ups) == 1:
        context['upstream'] = ups[0]
    context['can_edit_member'] = self.request.user.has_perm('amber.edit_member')
    context['now'] = timezone.now()
    return context

class MemberCreateView(PermissionRequiredMixin, CreateView):
  model = Member
  template_name_suffix = '_create_form'
  fields = ['name', 'nick', 'email', 'wechat', 'source', 'upstream', 'mobile', 'phone', 'address', 'gender', 'birthday', 'rank', 'tag', 'portrait']
  permission_required = 'amber.edit_member'
  
  def form_valid(self, form):
    obj = form.save(commit = False)
    ups = obj.upstream
    users = Member.objects.all()
    obj.upstream = ups if any([ ups == x.mobile for x in users ]) else 0
    # if upstream, 添加积分
    obj.save()
    return super(MemberCreateView, self).form_valid(form)

class MemberUpdateView(PermissionRequiredMixin, UpdateView):
  model = Member
  template_name_suffix = '_update_form'
  fields = ['name', 'nick', 'email', 'wechat', 'source', 'phone', 'address', 'rank', 'tag', 'status', 'portrait']
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
    context['bylist'] = list(set([ x.inb.by for x in context['object_list']]))
    ol = context['object_list']
    date__year = self.request.GET.get('date__year')
    date__year = None if date__year == 'C' else date__year
    date__month = self.request.GET.get('date__month')
    date__month = None if date__month == 'C' else date__month
    kind = self.request.GET.get('kind')
    kind = None if kind == 'C' else kind
    type = self.request.GET.get('type')
    type = None if type == 'C' else type
    by = self.request.GET.get('by')
    by = None if by == 'C' else by
    pr = self.request.GET.get('pr')
    pr = None if pr == 'C' else pr
    ktype = self.request.GET.get('ktype')
    ktype = None if ktype == 'C' else ktype
    status = self.request.GET.get('status')
    status = None if status == 'C' else status
    order_by = self.request.GET.get('o')
    q = self.request.GET.get('q')
    context['get_str'] = ''
    # query
    if (q):
      l = []
      for i in ol:
        if (q in i.inb.name) or (q in i.inb) or (q in i.inb.by) or (i.inb.tag and q in i.inb.tag) or (i.tag and q in i.tag):
          l.append(i)
      ol = l
      context['q'] = l
    # filter
    if (date__year):
      ol = [ x for x in ol if x.inb.date.year == int(date__year) ]
      context['get_str'] += ('&date__year=' + date__year)
      context['y'] = int(date__year)
    if (date__month):
      ol = [ x for x in ol if x.inb.date.month == int(date__month) ]
      context['get_str'] += ('&date__month=' + date__month)
      context['m'] = int(date__month)
    if (kind):
      ol = [ x for x in ol if x.inb.kind == int(kind) ]
      context['get_str'] += ('&kind=' + kind)
      context['k'] = int(kind)
    if (type):
      ol = [ x for x in ol if x.inb.type == int(type) ]
      context['get_str'] += ('&type=' + type)
      context['t'] = int(type)
    if (by):
      ol = [ x for x in ol if x.inb.by == by ]
      context['get_str'] += ('&by=' + by)
      context['b'] = by
    if (pr):
      ol = [ x for x in ol if x.inb.provider == pr ]
      context['get_str'] += ('&pr=' + pr)
      context['p'] = pr
    if (ktype):
      ol = [ x for x in ol if x.inb.ktype == int(ktype) ]
      context['get_str'] += ('&ktype=' + ktype)
      context['kt'] = int(ktype)
    if (status):
      ol = [ x for x in ol if x.status == int(status) ]
      context['get_str'] += ('&status=' + status)
      context['s'] = int(status)
    # order
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
      elif (order == 40):
        ol = sorted(ol, key=lambda i: i.inb.where)
      elif (order == 5):
        ol = sorted(ol, key=lambda i: i.remains)
      elif (order == 6):
        pass
      elif (order == 7):
        ol = sorted(ol, key=lambda i: i.inb.baseprice)
      elif (order == 8):
        ol = sorted(ol, key=lambda i: i.inb.saleprice)
      elif (order == 80):
        ol = sorted(ol, key=lambda i: i.inb.tprice)
      elif (order == 9):
        ol = sorted(ol, key=lambda i: i.inb.date)
      elif (order == 10):
        ol = sorted(ol, key=lambda i: i.inb.ktype)
      elif (order == 11):
        ol = sorted(ol, key=lambda i: i.status)
      if (order_by < 0):
        ol.reverse()
      context['order_by'] = order_by
    context['object_list'] = ol
    context['can_in'] = self.request.user.has_perm('amber.canin')
    context['can_viewbase'] = self.request.user.has_perm('amber.viewbase')
    context['can_out'] = self.request.user.has_perm('amber.canout')
    context['now'] = timezone.now()
    context['dummy'] = '导出到csv'
    return context
    
class StoreDetailView(LoginRequiredMixin, DetailView):
  model = Store
  def get_context_data(self, **kwargs):
    context = super(StoreDetailView, self).get_context_data(**kwargs)
    store = context['store']
    context['imgs'] = StoreImage.objects.filter(store=store.id)
    context['outbounds'] = OutBound.objects.filter(store=store.id)
    context['can_viewbase'] = self.request.user.has_perm('amber.viewbase')
    context['can_in'] = self.request.user.has_perm('amber.canin')
    context['can_out'] = self.request.user.has_perm('amber.canout')
    context['now'] = timezone.now()
    return context

class InBoundSheetView(PermissionRequiredMixin, DetailView):
  model = InBound
  permission_required = 'amber.canin'
    
class InBoundCreateView(PermissionRequiredMixin, CreateView):
  model = InBound
  template_name_suffix = '_create_form'
  fields = ['name', 'kind', 'type', 'where', 'quantity', 'qunit', 'weight', 'wunit', 'baseprice', 'saleprice', 'tprice', 'tweight'
          , 'provider', 'length', 'diameter', 'ktype', 'tag']
  permission_required = 'amber.canin'

  def form_valid(self, form):
    obj = form.save(commit = False)
    obj.by = str(self.request.user)
    if obj.tweight == 0:
      obj.tweight = obj.weight * obj.quantity
    if obj.tprice == 0:
      obj.tprice = obj.saleprice * obj.quantity
    obj.save()
    Store(inb=obj, remains=obj.quantity).save()
    return super(InBoundCreateView, self).form_valid(form)

class StoreImageView(PermissionRequiredMixin, CreateView):
  model = StoreImage
  template_name_suffix = '_create_form'
  fields = ['image']
  permission_required = 'amber.canin'
    
  def form_valid(self, form):
    obj = form.save(commit = False)
    obj.store = Store.objects.filter(id=self.kwargs['store_id'])[0]
    obj.save()
    return super(StoreImageView, self).form_valid(form)

class OutBoundCreateView(PermissionRequiredMixin, CreateView):
  model = OutBound
  template_name_suffix = '_create_form'
  fields = ['quantity', 'price', 'people', 'payment', 'cost', 'producer', 'type', 'tag']
  permission_required = 'amber.canout'

  def get_context_data(self, **kwargs):
    context = super(OutBoundCreateView, self).get_context_data(**kwargs)
    context['store'] = Store.objects.filter(id=self.kwargs['store_id'])[0]
    return context

  def form_valid(self, form):
    obj = form.save(commit = False)
    obj.store = Store.objects.filter(id=self.kwargs['store_id'])[0]
    obj.by = str(self.request.user)
    obj.price = obj.store.final_price()
    obj.store.remains = obj.store.remains - obj.quantity
    try:
      m = int(obj.people)
      ml = Member.objects.filter(mobile=m)
      if (len(ml)):
        obj.member = ml[0]
        obj.people = str(obj.member)
    except ValueError:
      pass
    
    if (obj.store.remains == 0):
      obj.store.status = 1
    obj.store.save()
    obj.save()
    ''' one submit, multiple saves!!!
    obj2 = form.save(commit = False)
    obj2.pk = None
    obj2.save()
    '''
    return super(OutBoundCreateView, self).form_valid(form)

# Craft ==================================================================================
class CraftCreateView(PermissionRequiredMixin, CreateView):
  model = CraftSheet
  template_name_suffix = '_create_form'
  fields = ['edate', 'desc', 'producer', 'tag']
  permission_required = 'amber.canout'

  def form_valid(self, form):
    #stores = self.request.POST.getlist('stores_old') + self.request.POST.getlist('stores')
    obj = form.save(commit = False)
    obj.by = str(self.request.user)
    obj.save()
    
    obs = self.request.GET.getlist('outbounds')
    for o in obs:
      ob = OutBound.objects.filter(id=o)[0]
      ob.craft = obj
      ob.type = 2
      ob.save()
    return super(CraftCreateView, self).form_valid(form)
    
class CraftDetailView(LoginRequiredMixin, DetailView):
  model = CraftSheet
  def get_context_data(self, **kwargs):
    context = super(CraftDetailView, self).get_context_data(**kwargs)
    craft = context['craftsheet']
    context['outbounds'] = OutBound.objects.filter(craft=craft.id)
    context['can_viewbase'] = self.request.user.has_perm('amber.viewbase')
    context['can_in'] = self.request.user.has_perm('amber.canin')
    context['can_out'] = self.request.user.has_perm('amber.canout')
    context['now'] = timezone.now()
    return context

class CraftListView(LoginRequiredMixin, ListView):
  model = CraftSheet

  def get_context_data(self, **kwargs):
    context = super(CraftListView, self).get_context_data(**kwargs)

    context['ylist'] = list(set([ x.cdate.year for x in context['object_list']]))
    context['bylist'] = list(set([ x.by for x in context['object_list']]))
    ol = context['object_list']
    date__year = self.request.GET.get('date__year')
    date__year = None if date__year == 'C' else date__year
    date__month = self.request.GET.get('date__month')
    date__month = None if date__month == 'C' else date__month
    by = self.request.GET.get('by')
    by = None if by == 'C' else by
    order_by = self.request.GET.get('o')
    q = self.request.GET.get('q')
    context['get_str'] = ''
    # query

    # filter
    if (date__year):
      ol = [ x for x in ol if x.cdate.year == int(date__year) ]
      context['get_str'] += ('&date__year=' + date__year)
      context['y'] = int(date__year)
    if (date__month):
      ol = [ x for x in ol if x.cdate.month == int(date__month) ]
      context['get_str'] += ('&date__month=' + date__month)
      context['m'] = int(date__month)
    # order
    if (order_by):
      order_by = int(order_by)
      order = abs(order_by)
      if (order == 1):
        ol = sorted(ol, key=lambda i: i.id)
      elif (order == 2):
        ol = sorted(ol, key=lambda i: i.cdate)
      elif (order == 3):
        ol = sorted(ol, key=lambda i: i.ddate)
      elif (order == 4):
        ol = sorted(ol, key=lambda i: i.sdate)
      elif (order == 5):
        ol = sorted(ol, key=lambda i: i.edate)
      elif (order == 6):
        ol = sorted(ol, key=lambda i: i.adate)
      if (order_by < 0):
        ol.reverse()
      context['order_by'] = order_by
    context['object_list'] = ol
    context['can_in'] = self.request.user.has_perm('amber.canin')
    context['can_viewbase'] = self.request.user.has_perm('amber.viewbase')
    context['can_out'] = self.request.user.has_perm('amber.canout')
    context['now'] = timezone.now()
    context['dummy'] = '导出到csv'
    return context

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
  context['pending_outbound']  = OutBound.objects.filter(type=0)
  context['dummy'] = 'testing'
  return render(request, 'amber/index.html', context)
  
@login_required()
def return_outbound(request):
  context = {}
  context['now'] = timezone.now()
  group = 'none'
  if (len(request.user.groups.all()) > 0):
    group = str(request.user.groups.all()[0]).lower()
  context['is_group_finance']  = group == 'finance'
  context['is_group_designer'] = group == 'designer'
  context['is_group_sales']    = group == 'sales'
  context['pending_outbound']  = OutBound.objects.filter(type=0)
  context['dummy'] = 'return_outbound'
  return render(request, 'amber/index.html', context)

@login_required()
def print_stores(request):
  context = {}
  context['now'] = timezone.now()
  ll = str(request.GET.get('items')).split('_')
  try:
    ll = [ int(x) for x in ll ]
  except ValueError:
    ll = []
  context['dummy'] = ll
  context['ol'] = Store.objects.filter(id__in=ll)
  context['can_viewbase'] = request.user.has_perm('amber.viewbase')
  return render(request, 'amber/print_stores.html', context)

@login_required()
def print_stores_lite(request):
  context = {}
  context['now'] = timezone.now()
  ll = str(request.GET.get('items')).split('_')
  try:
    ll = [ int(x) for x in ll ]
  except ValueError:
    ll = []
  context['ol'] = Store.objects.filter(id__in=ll)
  imgs = StoreImage.objects.all()
  all_imgs = [ x for x in imgs if x.store.id in ll ]
  img_store_ids = []
  single_imgs = []
  for img in all_imgs:
    if not (img.store.id in img_store_ids):
      img_store_ids.append(img.store.id)
      single_imgs.append(img)
  context['imgs'] = single_imgs
  context['dummy'] = context['imgs']
  return render(request, 'amber/print_stores_lite.html', context)

@login_required()
def print_crafts(request):
  context = {}
  context['now'] = timezone.now()
  ll = str(request.GET.get('items')).split('_')
  try:
    ll = [ int(x) for x in ll ]
  except ValueError:
    ll = []
  context['dummy'] = ll
  context['ol'] = CraftSheet.objects.filter(id__in=ll)
  context['can_viewbase'] = request.user.has_perm('amber.viewbase')
  return render(request, 'amber/print_crafts.html', context)