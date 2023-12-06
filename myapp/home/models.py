from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_default_curfew_time():
    return timezone.now().time()


    
class Hostel(models.Model):
    
    name = models.CharField(max_length=255)
    address = models.TextField()
    owner_name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    total_capacity = models.PositiveIntegerField()
    current_vacancy = models.PositiveIntegerField()
    
    mens_or_ladies = models.CharField(max_length=10)
    average_rent = models.PositiveIntegerField()
    
    accommodation_type = models.CharField(max_length=10)
    curfew = models.TimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    mess=models.TextField(default=None, blank=True, null=True)
    distance=models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Grievance(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    semester = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    hostel = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    complaint_text = models.TextField()
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_status = models.CharField(max_length=255, default="Pending")
    complaint_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name





