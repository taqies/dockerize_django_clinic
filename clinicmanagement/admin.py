from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.

from .models import Patient, Record

@admin.register(Patient)
class PatientModelAdmin(VersionAdmin):
    pass

@admin.register(Record)
class RecordModelAdmin(VersionAdmin):
    pass
