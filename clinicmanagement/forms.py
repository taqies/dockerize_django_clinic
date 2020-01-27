from django import forms
from django.utils import timezone
from .models import Patient, Record,Maternity

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

class MaternityForm(forms.ModelForm):
    class Meta:
        model = Maternity
        fields = [
             'MRN','gestation_on_date_entered', 'estimated_due_date',
        ]

        widgets ={
            'estimated_due_date':forms.DateInput(format=('%d/%m/%Y'),attrs={'type':'date'})
        }

class UpdateMaternityForm(forms.ModelForm):
    class Meta:
        model = Maternity
        fields = [
           'is_delivered','delivered_on'
        ]

        widgets ={
            'delivered_on':forms.DateInput(format=('%d/%m/%Y'),attrs={'type':'date'})
        }