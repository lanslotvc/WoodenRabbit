from django.db import models

# Create your models here.

# IMPORTANT!!!
# run the followings upon changes to models:
# python manage.py makemigrations dym
# python manage.py sqlmigrate dym 0001   # (just show schemas)
# python manage.py migrate

class Member(models.Model):
  name = models.TextField('客户姓名')
  email = models.EmailField('客户邮箱')
  mobile = models.IntegerField('手机', default=0)
  phone = models.IntegerField('座机', default=0)
  address = models.TextField('地址')
  gender = models.CharField('性别', max_length=1)
  join_date = models.DateTimeField('加入会员日期')
  birthday = models.DateTimeField('生日')
  accumulates = models.IntegerField('累积消费', default=0)
  n_purchase_orders = models.IntegerField('累积销售订单', default=0)
  n_craft_orders = models.IntegerField('累积制作订单', default=0)
  rank = models.IntegerField('VIP等级', default=0)
  status = models.IntegerField('客户状态', default=0)
  tag = models.TextField('备注', blank=True, null=True)

  def __str__(self):
    return self.name
    
class TestOrder(models.Model):
  member = models.ForeignKey(Member, models.SET_NULL, blank=True, null=True)
  create_date = models.DateTimeField('Order begin date')
  status = models.IntegerField('Order status', default=0)