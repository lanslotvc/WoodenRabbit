import datetime
from django.utils import timezone
from django.db import models
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.

# IMPORTANT!!!
# run the followings upon changes to models:
# python manage.py makemigrations amber
# python manage.py sqlmigrate amber 0001   # (just show schemas)
# python manage.py migrate

class Member(models.Model):
  class Meta:
    permissions = (
                    ("edit_member", "Can add/change/delete members"),
                  )
  rank_choice = ((0, '普通会员'), (1, '高级会员'), (2, '至尊会员'))
  status_choice = ((0, '已退'), (1, '活跃'))
  gender_choice = ((0, '美女'), (1, '帅哥'))
  source_choice = ((0, '其他'), (1, '会员介绍'), (2, '店面客人'), (3, '网络推广'), (4, '展会'))
  
  name = models.CharField('姓名', max_length=32)
  nick = models.CharField('昵称', max_length=64)
  wechat = models.CharField('微信号', max_length=64)
  source = models.IntegerField('来源', default=0, choices=source_choice)
  upstream = models.IntegerField('介绍人', default=0)
  email = models.EmailField('邮箱', blank=True, null=True)
  mobile = models.IntegerField('手机', default=0, unique=True)
  phone = models.IntegerField('座机', default=0, blank=True, null=True)
  address = models.TextField('地址', blank=True, null=True)
  gender = models.IntegerField('性别', default=0, choices=gender_choice)
  join_date = models.DateField('加入会员日期', default=timezone.now)
  birthday = models.DateField('生日')
  accumulates = models.IntegerField('累积消费', default=0)
  ds_acc = models.IntegerField('下线累积消费', default=0)
  n_purchase_orders = models.IntegerField('累积销售订单', default=0)
  n_craft_orders = models.IntegerField('累积制作订单', default=0)
  rank = models.IntegerField('VIP等级', default=0, choices=rank_choice)
  status = models.IntegerField('会员状态', default=1, choices=status_choice)
  tag = models.TextField('备注', blank=True, null=True)
  portrait = models.ImageField('照片', upload_to='upload', blank=True, null=True)
  # 生日提醒
  # 等级自动计算
  # 介绍人 optional
  # 发展下线 accumulate
  # 第一单优惠 accumulates == 0
  # 字段：积分，推荐人积分
  
  def _next_birth(self):
    today = timezone.now().replace(tzinfo=None)
    next = datetime.datetime(today.year, self.birthday.month, self.birthday.day, 0, 0)
    today = datetime.datetime(today.year, today.month, today.day, 0, 0)
    if (today > next):
      next = datetime.datetime(today.year + 1, self.birthday.month, self.birthday.day, 0, 0)
    return (next - today).days

  def next_birthday(self):
    d = self._next_birth()
    c = 'BB0000' if d < 60 else '000000'
    if d < 10:
      a = ' <!!!>'
    elif d < 30:
      a = ' <!!>'
    elif d < 60:
      a = ' <!>'
    else:
      a = ''
    return format_html('<span style="color: #{};">{}{}</span>', c, d, a)
  next_birthday.allow_tags = True
  next_birthday.short_description = '下个生日'
  
  def decro_portrait(self):
    if (not self.portrait):
      return format_html('<p>不给看～～</p>')
    return format_html('<img src="/amber{0}" alt="" height=120 width=90 />', self.portrait.url)
  decro_portrait.allow_tags = True
  decro_portrait.short_description = '靓照'

  def __str__(self):
    return self.name + '  [ ' + self.get_gender_display() + ', ' + self.get_rank_display() + ', ' + self.get_status_display() + ' ]'
    
  def get_absolute_url(self):
    return reverse('amber:member', kwargs={'pk': self.pk})

class InBound(models.Model):
  class Meta:
    permissions = (
                    ("canin", "WR: Can add/change/delete inbound sheet"),
                    ("viewbase", "WR: Can access base price"),
                  )

  kind_choice = ((0, '珍珠'), (1, '翡翠'), (2, '白玉'), (3, '彩宝'), (4, '钻石'), (5, '文玩'), (6, '素金'), (7, '古董珠宝'), (8, '瓷器'), (9, '裸链'), (10, '珊瑚'), (11, '玉石'), (12, '半宝'), (999, '其他'))
  type_choice = ((0, '成品'), (1, '原石'), (2, '裸链'), (3, 'K金配件'), (4, '客供制作'), (5, '手工配件'), (6, '配石'), (7, '配件'), (8, '其他配件'), (9, '珍珠'), (10, '古董'), (999, '其他'))
  where_choice = ((0, '冬君'), (1, '店面'), (2, '设计师'), (3, '其他'))
  ktype_choice = ((0, '18K红'), (1, '18K黄'), (2, '18K白'), (3, 'PT950'), (4, 'PT900'), (5, 'PT850'), (6, '14K红'), (7, '14K黄')
                , (8, '14K白'), (9, '10K黄'), (10, '10K白'), (11, '24K'), (12, '925银'), (999, '其他'), (9999, '不适用'))
  
  name = models.CharField('名称', max_length=64)
  seq  = models.CharField('编号', max_length=16, blank=True, null=True)
  kind = models.IntegerField('类别', default=999, choices=kind_choice)
  type = models.IntegerField('库存类型', default=0, choices=type_choice)
  where = models.IntegerField('库号', default=0, choices=where_choice)
  
  quantity = models.IntegerField('数量', default=0)
  qunit = models.CharField('数量单位', max_length=16, blank=True, null=True)
  weight = models.FloatField('重量', default=0.0)
  wunit = models.CharField('重量单位', max_length=16, blank=True, null=True)
  baseprice = models.IntegerField('单价', default=0, blank=True, null=True)
  saleprice = models.IntegerField('售价', default=0, blank=True, null=True)
  tweight = models.IntegerField('总重', default=0)
  tprice = models.IntegerField('总价', default=0)
  
  provider = models.CharField('供应商', max_length=128, blank=True, null=True)
  date = models.DateField('入库日期', default=timezone.now)
  by = models.CharField('经手人', max_length=128)
  
  length = models.CharField('长度', max_length=64, blank=True, null=True)
  diameter = models.CharField('直径度', max_length=64, blank=True, null=True)
  ktype = models.IntegerField('K金类别', default=9999, choices=ktype_choice)

  tag = models.TextField('备注', blank=True, null=True)

  def __str__(self):
    return '入库单_' + str(self.id)
  def get_absolute_url(self):
    return reverse('amber:store_list')

class Store(models.Model):
  status_choice = ((0, '正常'), (1, '已出库'), (2, '找不到了>.<'))
  
  inb = models.ForeignKey(InBound, models.SET_NULL, blank=True, null=True)
  remains = models.IntegerField('剩余', default=0)
  status = models.IntegerField('状态', default=0, choices=status_choice)
  discount = models.IntegerField('折扣', default=100)
  bestsale = models.IntegerField('特价', default=0)

  tag = models.TextField('备注', blank=True, null=True)
  
  def __str__(self):
    return '库存_' + str(self.inb.id) if self.inb else '库存_找不到入库单啊！'
  def final_price(self):
    price = self.inb.saleprice
    if (self.bestsale != 0):
      return self.bestsale
    if (self.discount > 0 and self.discount < 100):
      return int(price * self.discount / 100)
    return price

class StoreImage(models.Model):
  store = models.ForeignKey(Store, models.SET_NULL, blank=True, null=True)
  image = models.ImageField('照片', upload_to='upload/store', blank=True, null=True)
  
  def get_absolute_url(self):
    return reverse('amber:store', kwargs={'pk': self.store.pk})

class CraftSheet(models.Model):
  cdate = models.DateField('订制日期', default=timezone.now)
  ddate = models.DateField('设计日期', default=timezone.now, blank=True, null=True)
  sdate = models.DateField('送厂日期', default=timezone.now, blank=True, null=True)
  edate = models.DateField('预计完成日期', default=timezone.now, blank=True, null=True)
  adate = models.DateField('实际完成日期', default=timezone.now, blank=True, null=True)
  producer = models.CharField('制作方', max_length=128, blank=True, null=True)
  by = models.CharField('经手人', max_length=128)
  desc = models.TextField('制作描述', blank=True, null=True)
  tag = models.TextField('备注', blank=True, null=True)

  def get_absolute_url(self):
    return reverse('amber:craft_list')
  def __str__(self):
    return '生产单_' + str(self.id)
    
class OutBound(models.Model):
  class Meta:
    permissions = (
                    ("canout", "WR: Can operate on outbound sheet"),
                  )

  type_choice = ((0, '未限定'), (1, '销售'), (2, '生产'))
  pay_choice = ((0, '现金'), (1, '信用卡'), (2, '支付宝'), (3, '微信'), (9, '其他'))
  rec_choice = ((0, '否'), (1, '是'))
  
  store = models.ForeignKey(Store, models.SET_NULL, blank=True, null=True)
  quantity = models.IntegerField('数量', default=0)
  date = models.DateField('出库日期', default=timezone.now)
  by = models.CharField('经手人', max_length=128)
  price = models.IntegerField('售价', default=0)
  member = models.ForeignKey(Member, models.SET_NULL, blank=True, null=True)
  people = models.CharField('客户名（VIP输入手机可关联）', max_length=128, blank=True, null=True)
  payment = models.IntegerField('付款方式', default=0, choices=pay_choice)
  cost = models.IntegerField('生产费用', default=0)
  producer = models.CharField('制作商', max_length=128, blank=True, null=True)
  tag = models.TextField('备注', blank=True, null=True)

  recraft = models.IntegerField('是否重新制作', default=0, choices=rec_choice)
  type = models.IntegerField('出库类型', default=0, choices=type_choice)
  craft = models.ForeignKey(CraftSheet, models.SET_NULL, blank=True, null=True)

  def __str__(self):
    ret = ''
    if self.type == 0:
      ret = '出库单_'
    elif self.type == 1:
      ret = '出库销售单_'
    elif self.type == 2:
      ret = '出库生产单_'
    return ret + str(self.id)
  def get_absolute_url(self):
    return reverse('amber:store', kwargs={'pk': self.store.pk})





