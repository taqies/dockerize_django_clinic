import io

from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from .models import Invoice, Service


def save_model(self, request, obj, form, change):
    if not obj.pk:
        # Only set added_by during the first save.
        #generate the invoice too
        obj.created_by = request.user
    super().save_model(request, obj, form, change)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    change_form_template = "admin/invoice_changeform.html"
    list_display=['patient','total_net_amount','discount','created_on','paid_on']
    list_filter =['is_paid']
    exclude =['created_by']

    def generate_invoice(self):
        pass


admin.site.register(Service)