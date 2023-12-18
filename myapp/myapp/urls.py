from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Add this import for the static function

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path('hostel', include('home.urls')),
    path('pageadmin', include('home.urls')),
    path('login', include('home.urls')),
    path('logout', include('home.urls')),
    path('grievance', include('home.urls')),
    path('commit_complaint', include('home.urls')),
    path('administration', include('home.urls')),
    path('insert', include('home.urls')),
    path('admin_complaint_view', include('home.urls')),
    path('status/<id>', include('home.urls')),
    path('bulkadd', include('home.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
