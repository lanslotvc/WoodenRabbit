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
  rank_choice = ((0, '普通会员'), (1, '高级会员'), (2, '至尊会员'))
  status_choice = ((0, '已退'), (1, '活跃'))
  gender_choice = (('F', '美女'), ('M', '帅哥'))
  
  name = models.CharField('客户姓名', max_length=32)
  email = models.EmailField('客户邮箱')
  mobile = models.IntegerField('手机', default=0)
  phone = models.IntegerField('座机', default=0)
  address = models.TextField('地址')
  gender = models.CharField('性别', max_length=1, choices=gender_choice)
  join_date = models.DateTimeField('加入会员日期', default=timezone.now)
  birthday = models.DateTimeField('生日')
  accumulates = models.IntegerField('累积消费', default=0)
  n_purchase_orders = models.IntegerField('累积销售订单', default=0)
  n_craft_orders = models.IntegerField('累积制作订单', default=0)
  rank = models.IntegerField('VIP等级', default=0, choices=rank_choice)
  status = models.IntegerField('客户状态', default=1, choices=status_choice)
  tag = models.TextField('备注', blank=True, null=True)
  portrait = models.ImageField('照片', upload_to='upload', blank=True, null=True)
  
  def decro_gender(self):
    return format_html('<span style="color: #BB00BB;">{0}</span>',
                       '帅哥' if self.gender == 'M' else '美女')
  decro_gender.allow_tags = True
  decro_gender.short_description = '性别'
  
  def decro_protrait(self):
    if (not self.portrait):
      return format_html('<p>不给看～～</p>')
    return format_html('<img src="/amber{0}" alt="" height=120 width=90 />', self.portrait.url)
  decro_protrait.allow_tags = True
  decro_protrait.short_description = '靓照'

  def backlink(self):
    return format_html('<a href="/amber/member/{0}/">返回</a>', self.id)
  backlink.allow_tags = True
  backlink.short_description = '回到列表'

  def __str__(self):
    return self.name + '  [ ' + self.get_gender_display() + ', ' + self.get_rank_display() + ', ' + self.get_status_display() + ' ]'
    
  def get_absolute_url(self):
    return reverse('amber:member', kwargs={'pk': self.pk})



class Material(models.Model):
  name = models.TextField('命名')
  kind = models.TextField('种类')
  type = models.IntegerField('（原材料/配件/成品/客带）', default=0)

  type_str_dic = {0: '原材料', 1: '配件', 2: '成品', 3: '客带'}
  def type_str(self):
    return Material.type_str_dic[self.type]
  
    
class TestOrder(models.Model):
  member = models.ForeignKey(Member, models.SET_NULL, blank=True, null=True)
  order_id = models.IntegerField('Order print id', default=0)
  create_date = models.DateTimeField('Order begin date')
  status = models.IntegerField('Order status', default=0)
  
  
  
  
  
  
  
  
  