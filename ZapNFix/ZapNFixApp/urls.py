"""ZapNFix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views
from django.conf.urls.static import static

from django.conf import settings


urlpatterns = [
    path('', views.index_page, name='home'),
    path('services/', views.services_page, name='about_page'),
    path('list/delete/<int:id>/', views.ClientRepairDelete, name='ClientRepairDelete'),
    path('list/edit/<int:id>/', views.ClientRepairEdit, name='ClientRepairEdit'),
    path('list/search/', views.repair_list_search, name='repair_list_search'),
    path('admin/', admin.site.urls),
    path('list/', views.list_page, name='list'),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('Repair/', views.ClientRepairApi, name="RepairList"),
    path('Repair/<int:pk>/', views.ClientRepairApi),
    path('Repair/SavePhoto/',views.SavePhoto),
    path('Repair/Delete/<int:id>', views.ClientRepairDelete),
    path('Repair/Feedback/<int:id>', views.Feeback),
    path('AddRequest/', views.addRequest, name="AddRequest"),
    path('AddRequest/AddPicture/',views.addPicture,name="AddPicture"),
    path('AddRequest/FilterBrand', views.FilterBrand, name="FilterBrand")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)