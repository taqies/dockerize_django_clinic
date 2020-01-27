from django.contrib import admin
from reversion.admin import VersionAdmin

# Register your models here.

from .models import Patient, Record, Maternity

@admin.register(Patient)
class PatientModelAdmin(VersionAdmin):
    pass

@admin.register(Record)
class RecordModelAdmin(VersionAdmin):
    pass


@admin.register(Maternity)
class RecordModelAdmin(VersionAdmin):
    pass
