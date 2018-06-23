"""ppx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from . import views
from .views import ContactView
from .views import MemberListView, MemberDetailView, MemberCreateView, MemberUpdateView
from .views import StoreListView, InBoundCreateView, StoreDetailView, StoreImageView, InBoundSheetView
from .views import OutBoundCreateView

app_name = 'amber'
urlpatterns = [
    path('',                        views.index,                  name='index'),
    path('contact/',                ContactView.as_view(),        name='contact'),
    path('member_list/',            MemberListView.as_view(),     name='member_list'),
    path('member/<pk>/',            MemberDetailView.as_view(),   name='member'),
    path('member_create/',          MemberCreateView.as_view(),   name='member_create'),
    path('member/<pk>/update',      MemberUpdateView.as_view(),   name='member_update'),
    
    path('store_list/',             StoreListView.as_view(),      name='store_list'),
    path('store/<pk>/',             StoreDetailView.as_view(),    name='store'),
    path('inbound/<pk>/',           InBoundSheetView.as_view(),   name='inbound'),
    path('inbound_create/',         InBoundCreateView.as_view(),  name='inbound_create'),
    path('store/<store_id>/upload', StoreImageView.as_view(),     name='store_image'),
    path('store/<store_id>/out',    OutBoundCreateView.as_view(), name='outbound_create'),
    path('print_stores/',           views.print_stores,           name='print_store_list'),
    
    path('login/',                  auth_views.LoginView.as_view(),                               name='login'),
    path('logout/',                 auth_views.LogoutView.as_view(),                              name='logout'),
    path('password_change/',        auth_views.PasswordChangeView.as_view(success_url='/amber/'), name='password_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()



