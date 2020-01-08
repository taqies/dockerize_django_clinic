from django.db import models
from django.contrib.auth.models import User
from clinicmanagement.models import Patient
from django.urls import reverse

# Create your models here.
class Service(models.Model):
    codename = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=6,
        decimal_places= 2,
        default = 0,
    )

    def __str__(self):
        return "{0} {1} price €{2}".format(str(self.codename),str(self.description),str(self.price))

class Invoice(models.Model):
    CREDITCARD = 'CC'
    CASH = 'CA'
    BANKTRANSFER = 'BT'
    DEBITCARD = 'DC'
    NA = 'NA'
    PAYMENT_TYPE_CHOICES = [
        (CREDITCARD, 'CREDIT CARD'),
        (CASH, 'CASH'),
        (BANKTRANSFER, 'BANK TRANSFER'),
        (DEBITCARD, 'DEBIT CARD'),
        (NA, 'NA'),        
    ] 

    total_gross_amount = models.DecimalField(
        max_digits = 19,
        decimal_places = 2,
        default=0,
    )
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, null=True)
    procedure = models.ForeignKey(Service, on_delete = models.SET_NULL, null=True)        
    services = models.CharField(max_length= 220)
    discount = models.DecimalField(
        max_digits = 2,
        decimal_places = 0,
        default = 0,
    )

    total_net_amount = models.DecimalField(
        max_digits = 19,
        decimal_places = 2,
        default=0,
    )

    payment_type =  models.CharField(
        max_length = 2,
        choices = PAYMENT_TYPE_CHOICES,
        default= NA,
        )

    is_paid = models.BooleanField(default=False)
    paid_on = models.DateField("Paid on", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    created_on = models.DateTimeField(auto_now_add = True, blank = True, null = True)

    def __str__(self):
        return "{0} is charged total amount of {1} on date {2}".format(str(self.patient),str(self.total_net_amount), self.created_on.strftime('%d/%m/%Y'))

    def total_amount(self):
        if (self.discount == 0):
            return self.total_gross_amount
        else:
            return  self.total_gross_amount - (self.discount/100 * self.total_gross_amount)

    def get_absolute_url(self):
        return reverse('invoice_detail', kwargs={'pk': self.pk})
