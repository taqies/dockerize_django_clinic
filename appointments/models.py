from django.db import models
from django.contrib.auth.models import User
from clinicmanagement.models import Patient


# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,  null=True)
    appointment_time = models.TimeField('Appointment time')
    appointment_date = models.DateField('Appointment date')
    is_checked_in = models.BooleanField()
    is_cancelled = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    created_by = models.ForeignKey(User, models.SET_NULL, blank = True, null = True)