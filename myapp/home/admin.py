from django.contrib import admin
from home.models import Hostel,Grievance
# Register your models here.
admin.site.register(Hostel)
admin.site.register(Grievance)

class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner_name', 'contact_details', 'current_vacancy', 'mens_or_ladies', 'average_rent', 'mess', 'distance', 'accommodation_type', 'curfew', 'longitude', 'latitude')
    search_fields = ('name', 'owner_name')
    list_filter = ('mens_or_ladies', 'accommodation_type', 'mess')
