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
from .views import ContactView, MemberListView, MemberDetailView, MemberCreateView, MemberUpdateView

app_name = 'amber'
urlpatterns = [
    path('',                     views.index,                name='index'),
    path('contact/',             ContactView.as_view(),      name='contact'),
    path('member_list/',         MemberListView.as_view(),   name='member_list'),
    path('member/<pk>/',         MemberDetailView.as_view(), name='member'),
    path('member_create',        MemberCreateView.as_view(), name='member_create'),
    path('member_update/<pk>',   MemberUpdateView.as_view(), name='member_update'),
    
    path('porders/',             views.porders,              name='porders'),
    path('porder/<int:p_id>/',   views.porder,               name='porder'),
    path('corders/',             views.corders,              name='corders'),
    path('corder/<int:c_id>/',   views.corder,               name='corder'),
    
    path('login/',               auth_views.LoginView.as_view(),          name='login'),
    path('logout/',              auth_views.LogoutView.as_view(),         name='logout'),
    path('password_change/',     auth_views.PasswordChangeView.as_view(success_url='/amber/'), name='password_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()



