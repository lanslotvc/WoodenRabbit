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
  email = models.EmailField('邮箱')
  mobile = models.IntegerField('手机', default=0, unique=True)
  phone = models.IntegerField('座机', default=0)
  address = models.TextField('地址')
  gender = models.IntegerField('性别', default=0, choices=gender_choice)
  join_date = models.DateTimeField('加入会员日期', default=timezone.now)
  birthday = models.DateTimeField('生日')
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
  '''
  kind_choice = ((, '白玉'), (, '翡翠'), (, '珍珠'), (, '钻石'), (, '红宝石'), (, '蓝宝石'), (, '祖母绿'), 
                 (, '尖晶石'), (, '琥珀'), (, '蜜蜡'), (, '欧珀'), (, '绿松石'), (, '舒俱来'), (, '海蓝宝'),
                 (, '月光石'), (, '拉长石'), (, '碧玺'), (, '玛瑙'), (, '珊瑚'), (, '碧玉'), (, '点翠'),
                 (, '青晶石'), (, '水晶'), (, '砗磲'), (, '芬达石'), (, '石榴石'), (, '海纹石'), (, '琉璃'),
                 (, '天珠'), (, '菩提子'), (, '沉香'), (, '红木'),
                 (, '黄金'), (, '铂金'), (, '白银'),
                 (9999, '其他'))
  '''
  kind_choice = ((0, '有机宝石'), (1, '无机宝石'), (2, '贵重金属'), (3, '贵重宝石'), (999, '其他'))
  type_choice = ((0, '成品'), (1, '原材料'), (2, '配件'), (3, '客带'))
  
  name = models.CharField('名称', max_length=64)
  desc = models.CharField('细别', max_length=128)
  kind = models.IntegerField('类别', default=999, choices=kind_choice)
  type = models.IntegerField('库存类型', default=1, choices=type_choice)
  
  quantity = models.IntegerField('数量', default=0)
  qunit = models.CharField('数量单位', max_length=16, blank=True, null=True)
  weight = models.IntegerField('重量', default=0)
  wunit = models.CharField('重量单位', max_length=16, blank=True, null=True)
  baseprice = models.IntegerField('成本', default=0)
  saleprice = models.IntegerField('售价', default=0)
  date = models.DateTimeField('入库日期', default=timezone.now)

  tag = models.TextField('备注', blank=True, null=True)

  def __str__(self):
    return '入库单_' + str(self.id)
  def get_absolute_url(self):
    return reverse('amber:store_list')

class Store(models.Model):
  inb = models.ForeignKey(InBound, models.SET_NULL, blank=True, null=True)
  remains = models.IntegerField('剩余', default=0)
  discount = models.IntegerField('折扣', default=0)
  bestsale = models.IntegerField('特价', default=0)

  tag = models.TextField('备注', blank=True, null=True)
  
  def __str__(self):
    return '库存_' + str(self.inb.id)

class StoreImage(models.Model):
  store = models.ForeignKey(Store, models.SET_NULL, blank=True, null=True)
  image = models.ImageField('照片', upload_to='upload/store', blank=True, null=True)
  
class OutBound(models.Model):
  pass

  
  
  
  
  
  
  
  
  
