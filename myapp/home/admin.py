from django.contrib import admin
from django.utils import timezone
from .models import Hostel, Grievance, Vacancy, HostelRequest


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    """Admin interface for Hostel model"""
    list_display = (
        'name', 'owner_name', 'contact_details', 'current_vacancy', 
        'mens_or_ladies', 'average_rent', 'approval_hostel_status'
    )
    list_filter = (
        'mens_or_ladies', 'accommodation_type', 'approval_hostel_status', 'mess'
    )
    search_fields = ('name', 'owner_name', 'address')
    readonly_fields = ('approval_hostel_status',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'owner_name', 'contact_details')
        }),
        ('Capacity & Rent', {
            'fields': ('total_capacity', 'current_vacancy', 'average_rent')
        }),
        ('Preferences & Facilities', {
            'fields': ('mens_or_ladies', 'accommodation_type', 'mess', 'curfew')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'distance')
        }),
        ('Approval', {
            'fields': ('approval_hostel_status',)
        }),
    )


@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    """Admin interface for Grievance model"""
    list_display = (
        'full_name', 'hostel', 'complaint_status', 'complaint_date'
    )
    list_filter = ('complaint_status', 'department', 'semester')
    search_fields = ('full_name', 'hostel', 'complaint_text')
    readonly_fields = ('complaint_date', 'complaint_time')
    fieldsets = (
        ('Student Information', {
            'fields': ('full_name', 'email', 'phone', 'semester', 'department')
        }),
        ('Complaint Details', {
            'fields': ('hostel', 'location', 'complaint_text')
        }),
        ('Status & Timing', {
            'fields': ('complaint_status', 'complaint_date', 'complaint_time')
        }),
    )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Admin interface for Vacancy model"""
    list_display = ('hostelname', 'vacancycount', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('hostelname',)
    readonly_fields = ('created_at',)
    actions = ['approve_vacancies', 'reject_vacancies']

    def approve_vacancies(self, request, queryset):
        """Bulk approve vacancy requests"""
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} vacancy requests approved.')
    approve_vacancies.short_description = "Approve selected vacancy requests"

    def reject_vacancies(self, request, queryset):
        """Bulk reject vacancy requests"""
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} vacancy requests rejected.')
    reject_vacancies.short_description = "Reject selected vacancy requests"


@admin.register(HostelRequest)
class HostelRequestAdmin(admin.ModelAdmin):
    """Admin interface for HostelRequest model"""
    list_display = (
        'name', 'owner_name', 'contact_details', 'approval_status', 
        'created_at', 'current_vacancy', 'average_rent'
    )
    list_filter = ('approval_status', 'mens_or_ladies', 'accommodation_type', 'mess', 'created_at')
    search_fields = ('name', 'owner_name', 'address', 'contact_details')
    readonly_fields = ('created_at', 'approved_at')
    actions = ['approve_hostel_requests', 'reject_hostel_requests']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'owner_name', 'contact_details')
        }),
        ('Capacity & Rent', {
            'fields': ('total_capacity', 'current_vacancy', 'average_rent')
        }),
        ('Preferences & Facilities', {
            'fields': ('mens_or_ladies', 'accommodation_type', 'mess', 'curfew')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'distance')
        }),
        ('Request Management', {
            'fields': ('approval_status', 'admin_notes', 'created_at', 'approved_at')
        }),
    )

    def approve_hostel_requests(self, request, queryset):
        """Bulk approve hostel requests and create hostel records"""
        approved_count = 0
        for hostel_request in queryset.filter(approval_status='Pending'):
            # Create a new Hostel record from the request
            new_hostel = Hostel.objects.create(
                name=hostel_request.name,
                address=hostel_request.address,
                owner_name=hostel_request.owner_name,
                contact_details=hostel_request.contact_details,
                total_capacity=hostel_request.total_capacity,
                current_vacancy=hostel_request.current_vacancy,
                mens_or_ladies=hostel_request.mens_or_ladies,
                average_rent=hostel_request.average_rent,
                accommodation_type=hostel_request.accommodation_type,
                curfew=hostel_request.curfew,
                longitude=hostel_request.longitude,
                latitude=hostel_request.latitude,
                distance=hostel_request.distance,
                mess=hostel_request.mess,
                approval_hostel_status='Approved'
            )
            
            # Update the request status
            hostel_request.approval_status = 'Approved'
            hostel_request.approved_at = timezone.now()
            hostel_request.save()
            approved_count += 1
            
        self.message_user(request, f'{approved_count} hostel requests approved and hostels created.')
    approve_hostel_requests.short_description = "Approve selected hostel requests"

    def reject_hostel_requests(self, request, queryset):
        """Bulk reject hostel requests"""
        updated = queryset.filter(approval_status='Pending').update(approval_status='Rejected')
        self.message_user(request, f'{updated} hostel requests rejected.')
    reject_hostel_requests.short_description = "Reject selected hostel requests"
