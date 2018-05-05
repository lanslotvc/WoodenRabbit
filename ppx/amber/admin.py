from django.contrib import admin

# Register your models here.
from .models import *

class MemberAdmin(admin.ModelAdmin):
  list_display=('name'
            #, 'email', 'mobile', 'phone', 'address'
            , 'gender'
            , 'accumulates', 'n_purchase_orders', 'n_craft_orders'
            , 'rank', 'status', 'decro_protrait'
            )
  list_editable = ['accumulates', 'n_purchase_orders', 'n_craft_orders']
  list_filter =('accumulates', 'n_purchase_orders', 'n_craft_orders', 'rank', 'status') #过滤器
  search_fields =('name', 'mobile', 'decro_gender', 'birthday') #搜索字段
  date_hierarchy = 'join_date'   # 详细时间分层筛选
  #exclude = ('birthday',)

class InBoundAdmin(admin.ModelAdmin):
  pass

class OutBoundAdmin(admin.ModelAdmin):
  pass

class StoreAdmin(admin.ModelAdmin):
  pass

admin.site.register(Member,   MemberAdmin)
admin.site.register(InBound,  InBoundAdmin)
admin.site.register(OutBound, OutBoundAdmin)
admin.site.register(Store,    StoreAdmin)
