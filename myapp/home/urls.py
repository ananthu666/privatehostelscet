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

    path('vaccancy',views.request_room,name='vaccancy'),
    path('approve_vacancy',views.approve_vacancy,name="approve_vacancy"),

  
    path('hostel_reg',views.hostel_reg , name='hostel_reg'),
    path('commit_hostel_reg', views.commit_hostel_reg , name = 'commit_hostel_reg'),
    path('hostel_approval', views.hostel_approval , name = 'hostel_approval'),
    path('hostel_status/<id>', views.hostel_status_view , name='hostel_status_view')
   

]
