from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
  
    path('', views.home, name='home'),
    path('hostel', views.hostel, name='hostel'),
    path('page_admin', views.page_admin, name='page_admin'),
    path('login', views.login_page, name='login'),
    path('logout', views.admin_logout, name='logout'),
    path('grievance', views.grievance, name='grievance'),
    path('commit_complaint', views.commit_complaint, name='commit_complaint'),
    path('administration', views.administration, name='administration'),
    path('insert', views.insert_hostel, name='insert_hostel'),
    path('admin_complaint_view', views.admin_complaint_view, name='admin_complaint_view'),
    path('status/<id>', views.status_view, name='status_view'),
    path('bulkadd', views.bulkadd, name='bulkadd'),
]
