from django.contrib import admin
from django.urls import path, include
from . import views
from .debug_views import test_view, debug_view

urlpatterns = [
    # Debug routes for Vercel testing
    path('test/', test_view, name='test'),
    path('debug/', debug_view, name='debug'),
    
    # Public pages
    path('', views.home, name='home'),
    path('hostel', views.hostel, name='hostel'),
    path('grievance', views.grievance, name='grievance'),
    path('commit_complaint', views.commit_complaint, name='commit_complaint'),
    
    # Hostel registration
    path('hostel_reg', views.hostel_reg, name='hostel_reg'),
    path('commit_hostel_reg', views.commit_hostel_reg, name='commit_hostel_reg'),
    
    # New hostel registration system
    path('hostel_registration', views.hostel_registration, name='hostel_registration'),
    path('submit_hostel_request', views.submit_hostel_request, name='submit_hostel_request'),
    
    # Vacancy management
    path('vaccancy', views.request_room, name='vaccancy'),
    path('approve_vacancy', views.approve_vacancy, name="approve_vacancy"),
    
    # Hostel request management
    path('approve_hostel_requests', views.approve_hostel_requests, name='approve_hostel_requests'),
    
    # Admin authentication
    path('page_admin', views.page_admin, name='page_admin'),
    path('login', views.login_page, name='login'),
    path('logout', views.admin_logout, name='logout'),
    
    # Admin panel
    path('administration', views.administration, name='administration'),
    path('insert', views.insert_hostel, name='insert_hostel'),
    path('admin_complaint_view', views.admin_complaint_view, name='admin_complaint_view'),
    path('hostel_approval', views.hostel_approval, name='hostel_approval'),
    
    # Status management
    path('status/<id>', views.status_view, name='status_view'),
    path('hostel_status/<id>', views.hostel_status_view, name='hostel_status_view'),
    
    # API endpoints
    path('api/search_hostels', views.search_hostels_api, name='search_hostels_api'),
    
    # Bulk operations
    path('bulkadd', views.bulkadd, name='bulkadd'),
]
