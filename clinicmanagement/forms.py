from django import forms
from django.utils import timezone
from .models import Patient, Record

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'email', 'address','address_line_2',
            'county','eircode','email',
            'contact_number', 'GP_name', 'GP_address'
            ]
        widgets ={
            'date_of_birth':forms.DateInput(format=('%d/%m/%Y'),attrs={'format': 'dd-mm-yyyy','type':'date',})
        }

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['date_of_clinic', 'referral_indication', 'parity',
            'smear','contraception','medical_history','surgical_history','medications','allergies',
            'current_symptoms', 'investigations_to_date','treatments_to_date',
            'examination_today','further_plan',    
            ]
        
        widgets ={
            'date_of_clinic':forms.DateInput(format=('%d/%m/%Y'),attrs={'class':'col-md-3','type':'date'})
        }

