"""rdb URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from app import views
import django_cas_ng.views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', login_required(views.search), name='search'),
    path('random/', login_required(views.random), name='random'),
    path('profile/', login_required(views.profile), name='profile'),
    path('admin/', admin.site.urls),
    path('accounts/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
]

urlpatterns += [
    path('lab/create/', views.LabCreate.as_view(), name='lab-create'),
    path('lab/<slug:slug>/', views.LabDetail.as_view(), name='lab-detail'),
    path('lab/<slug:slug>/update/', views.LabUpdate.as_view(), name='lab-update'),
    path('lab/<slug:slug>/delete/', views.LabDelete.as_view(), name='lab-delete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)