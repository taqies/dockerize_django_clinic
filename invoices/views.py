import io
import datetime
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from django.http import FileResponse
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Invoice
from .forms import InvoiceForm, UpdateInvoiceForm
from clinicmanagement.models import Patient
# Create your views here.

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    paginate_by = 20
    ordering ='-created_on'



class PatientInvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'

    def get_queryset(self):
        object_list = Invoice.objects.filter(
            Q(patient__pk=self.kwargs.get('pk'))
        ).order_by('-created_on')
        return object_list

class DetailInvoice (LoginRequiredMixin, ModelFormMixin, DetailView):
    model = Invoice
    form_class = UpdateInvoiceForm
    template = "invoices/detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self,form):
        
        return super(DetailInvoice,self).form_valid(form)

TOP_MARGIN=1.5 *  inch
BOTTOM_MARGIN = 1 * inch


def print_invoice(request,pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    buffer = io.BytesIO()
    #data needed for the invoice
    name = invoice.patient.first_name +' '+ invoice.patient.last_name
    address = invoice.patient.address
    county = invoice.patient.county
    date_created = invoice.created_on.strftime("%d-%m-%Y")
    total_gross_amount = invoice.total_gross_amount
    discount = invoice.discount
    total_net_amount = invoice.total_net_amount

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontsize = 10
    spacer = Spacer(0, 0.25*inch)


    story = []

    #address of patient
    story.append(Paragraph(name, styleN))
    story.append(Paragraph(address, styleN))
    story.append(Paragraph(county, styleN))
    story.append(spacer)
    story.append(Paragraph(date_created, styleN))
    



    #invoice details


    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin= TOP_MARGIN, bottomMargin=BOTTOM_MARGIN)
    
    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

