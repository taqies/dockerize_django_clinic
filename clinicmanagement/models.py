import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

ANTRIM = 'Antrim'
ARMAGH = 'Armagh'
CARLOW = 'Carlow'
CAVAN = 'Cavan'
CLARE = 'Clare'
CORK = 'Cork'
DERRY = 'Derry'
DONEGAL = 'Donegal'
DOWN = 'Down'
DUBLIN = 'Dublin'
FERMANAGH = 'Fermanagh'
GALWAY = 'Galway'
KERRY = 'Kerry'
KILDARE = 'Kildare'
KILKENNY = 'Kilkenny'
LAOIS = 'Laois'
LEITRIM = 'Leitrim'
LIMERICK = 'Limerick'
LONGFORD = 'Longford'
LOUTH = 'Louth'
MAYO = 'Mayo'
MEATH = 'Meath'
MONAGHAN = 'Monaghan'
OFFALY = 'Offaly'
ROSCOMMON = 'Roscommon'
SLIGO = 'Sligo'
TIPPERARY = 'Tipperary'
TYRONE = 'Tyrone'
WATERFORD = 'Waterford'
WESTMEATH = 'Westmeath'
WEXFORD = 'Wexford'
WICKLOW = 'Wicklow'
#county choices
COUNTY_CHOICES = [
        (ANTRIM,'ANTRIM'),
        (ARMAGH,'ARMAGH'),
        (CARLOW,'CARLOW'),
        (CAVAN,'CAVAN'),
        (CLARE,'CLARE'),
        (CORK,'CORK'),
        (DERRY,'DERRY'),
        (DONEGAL,'DONEGAL'),
        (DOWN,'DOWN'),
        (DUBLIN,'DUBLIN'),
        (FERMANAGH,'FERMANAGH'),
        (GALWAY,'GALWAY'),
        (KERRY,'KERRY'),
        (KILDARE,'KILDARE'),
        (KILKENNY,'KILKENNY'),
        (LAOIS,'LAOIS'),
        (LEITRIM,'LEITRIM'),
        (LIMERICK,'LIMERICK'),
        (LONGFORD,'LONGFORD'),
        (LOUTH,'LOUTH'),
        (MAYO,'MAYO'),
        (MEATH,'MEATH'),
        (MONAGHAN,'MONAGHAN'),
        (OFFALY,'OFFALY'),
        (ROSCOMMON,'ROSCOMMON'),
        (SLIGO,'SLIGO'),
        (TIPPERARY,'TIPPERARY'),
        (TYRONE,'TYRONE'),
        (WATERFORD,'WATERFORD'),
        (WESTMEATH,'WESTMEATH'),
        (WEXFORD,'WEXFORD'),
        (WICKLOW,'WICKLOW'),
    ]
# Create your models here.
class Patient(models.Model):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    short_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length = 200)
    address_line_2 = models.CharField (max_length= 200, null=True, blank = True)
    county = models.CharField(max_length=12, choices=COUNTY_CHOICES, default=WATERFORD)
    eircode = models.CharField(max_length = 10, null=True, blank = True)
    date_of_birth = models.DateField("Date of Birth")
    email = models.EmailField()
    contact_number = models.CharField(max_length = 12)
    GP_name = models.CharField(max_length = 50)
    GP_address = models.CharField(max_length = 200)
    next_of_kin_name = models.CharField(max_length = 100)
    next_of_kin_contact_number = models.CharField(max_length = 12)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, models.SET_NULL, null = True, blank = True)
    entered_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return (self.first_name + ' '+self.last_name)

    
    def get_absolute_url(self):
        return reverse('patient_detail', kwargs={'pk': self.pk})
           
    @property
    def get_contact_number(self):
        return self.contact_number
    
    @property
    def get_address(self):
        return self.address
    
    def age(self):
        return int((timezone.now().date() - self.date_of_birth).days / 365.25)

class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, null = True, blank = True, related_name="record")
    date_of_clinic = models.DateField("date of clinic")
    referral_indication = models.CharField(max_length= 300, null = True)
    age = models.IntegerField(default=0, null= True)
    parity = models.CharField(max_length=150, null = True)
    smear = models.CharField(max_length=150, null =True)
    contraception = models.CharField(max_length=150, blank=True)
    medical_history = models.TextField(max_length=600, null = True)
    surgical_history = models.TextField(max_length=600, null = True)
    medications = models.CharField(max_length=300, blank=True)
    allergies = models.CharField(max_length=300, blank=True)
    current_symptoms = models.TextField(max_length=500, null=True)
    investigations_to_date = models.TextField(max_length=500, null=True)
    treatments_to_date = models.TextField(max_length=500, null = True)
    examination_today =  models.TextField(max_length=500, null=True)
    further_plan =  models.TextField(max_length=500, null=True)
    created_date = models.DateTimeField("date created", auto_now_add=True)

    def __str__(self):
        return "Patient Record of {0} clinic visit on {1}".format(str(self.patient), self.date_of_clinic.strftime('%d/%m/%Y'))

    def get_absolute_url(self):
        return reverse('patient_record', kwargs={'pk':self.patient.pk,'pk_r': self.pk})