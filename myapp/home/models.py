from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_default_curfew_time():
    """Get default curfew time (currently unused)"""
    return timezone.now().time()


class Hostel(models.Model):
    """Model representing a hostel"""
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Mixed', 'Mixed'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=255, help_text="Name of the hostel")
    address = models.TextField(help_text="Full address of the hostel")
    owner_name = models.CharField(max_length=255, help_text="Name of the hostel owner")
    contact_details = models.CharField(max_length=255, help_text="Contact information")
    total_capacity = models.PositiveIntegerField(default=0, help_text="Total bed capacity")
    current_vacancy = models.PositiveIntegerField(help_text="Currently available beds")
    mens_or_ladies = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Gender preference")
    average_rent = models.PositiveIntegerField(help_text="Average monthly rent")
    accommodation_type = models.CharField(max_length=50, help_text="Type of accommodation")
    curfew = models.TimeField(null=True, blank=True, help_text="Curfew time (optional)")
    longitude = models.FloatField(help_text="Longitude coordinate")
    latitude = models.FloatField(help_text="Latitude coordinate")
    mess = models.TextField(default=None, blank=True, null=True, help_text="Mess facility details")
    distance = models.FloatField(default=0.0, help_text="Distance from college in km")
    approval_hostel_status = models.CharField(
        max_length=255, 
        choices=APPROVAL_STATUS_CHOICES, 
        default="Pending",
        help_text="Approval status"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Hostel"
        verbose_name_plural = "Hostels"

    def __str__(self):
        return f"{self.name} - {self.owner_name}"


class Grievance(models.Model):
    """Model representing student grievances"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]
    
    full_name = models.CharField(max_length=255, help_text="Student's full name")
    email = models.EmailField(help_text="Student's email address")
    phone = models.CharField(max_length=20, help_text="Phone number")
    semester = models.CharField(max_length=255, help_text="Current semester")
    department = models.CharField(max_length=255, help_text="Department/course")
    hostel = models.CharField(max_length=255, help_text="Hostel name")
    location = models.CharField(max_length=255, help_text="Location/room details")
    complaint_text = models.TextField(help_text="Detailed complaint")
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_status = models.CharField(
        max_length=255, 
        choices=STATUS_CHOICES, 
        default="Pending",
        help_text="Complaint status"
    )
    complaint_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-complaint_date']
        verbose_name = "Grievance"
        verbose_name_plural = "Grievances"

    def __str__(self):
        return f"{self.full_name} - {self.complaint_status}"


class Vacancy(models.Model):
    """Model representing vacancy requests for hostels"""
    hostel = models.ForeignKey(
        Hostel, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="Related hostel (if exists)"
    )
    hostelname = models.CharField(max_length=255, help_text="Name of the hostel")
    vacancycount = models.PositiveIntegerField(help_text="Number of vacant rooms")
    approved = models.BooleanField(default=False, help_text="Approval status")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Vacancy Request"
        verbose_name_plural = "Vacancy Requests"

    def __str__(self):
        return f"{self.hostelname} - {self.vacancycount} rooms"


class HostelRequest(models.Model):
    """Model representing hostel registration requests from owners"""
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Mixed', 'Mixed'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255, help_text="Name of the hostel")
    address = models.TextField(help_text="Full address of the hostel")
    owner_name = models.CharField(max_length=255, help_text="Name of the hostel owner")
    contact_details = models.CharField(max_length=255, help_text="Contact information")
    
    # Capacity and Vacancy
    total_capacity = models.PositiveIntegerField(help_text="Total bed capacity")
    current_vacancy = models.PositiveIntegerField(help_text="Currently available beds")
    
    # Hostel Details
    mens_or_ladies = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Gender preference")
    average_rent = models.PositiveIntegerField(help_text="Average monthly rent")
    accommodation_type = models.CharField(max_length=50, help_text="Type of accommodation (Hostel/PG)")
    curfew = models.TimeField(null=True, blank=True, help_text="Curfew time (optional)")
    
    # Location
    longitude = models.FloatField(help_text="Longitude coordinate")
    latitude = models.FloatField(help_text="Latitude coordinate")
    distance = models.FloatField(default=0.0, help_text="Distance from college in km")
    
    # Additional Details
    mess = models.CharField(max_length=10, default="No", help_text="Mess facility availability (Yes/No)")
    
    # Request Management
    approval_status = models.CharField(
        max_length=255, 
        choices=APPROVAL_STATUS_CHOICES, 
        default="Pending",
        help_text="Request approval status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Additional notes from admin
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin notes or rejection reason")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Hostel Registration Request"
        verbose_name_plural = "Hostel Registration Requests"

    def __str__(self):
        return f"{self.name} - {self.owner_name} ({self.approval_status})"

