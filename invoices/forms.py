from django import forms

from .models import Invoice, Service

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['procedure','payment_type','is_paid', 'paid_on']
        widgets ={
            'paid_on':forms.DateInput(format=('%d/%m/%Y'),attrs={'format': 'dd-mm-yyyy','type':'date',})
        }

class UpdateInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['payment_type','is_paid', 'paid_on']
        widgets ={
            'paid_on':forms.DateInput(format=('%d/%m/%Y'),attrs={'format': 'dd-mm-yyyy','type':'date',})
        }