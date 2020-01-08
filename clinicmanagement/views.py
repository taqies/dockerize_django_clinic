import io
import uuid
import datetime
from reversion.views import RevisionMixin
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from django.http import FileResponse
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
from django.http import HttpResponse

from .models import Patient, Record
from .forms import PatientForm, RecordForm
from invoices.models import Invoice
from invoices.forms import InvoiceForm

class PatientListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Patient
    template_name = 'clinicmanagement/patient_list_view.html'
    queryset = Patient.objects.all().order_by('last_name')  # Default: Model.objects.all()


class PatientSearchResultsView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'clinicmanagement/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Patient.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('-entered_date')
        return object_list

class PatientDetailView(LoginRequiredMixin, DetailView):
   
    model = Patient

    ## Pass multiple models to the view
    def get_context_data(self, **kwargs):
        context= super(PatientDetailView,self).get_context_data(**kwargs)
        context['patient_record_list'] = Record.objects.filter(
            Q(patient__pk=self.object.id)
        ).order_by('-date_of_clinic')[:10]
        context['patient_invoices_list'] = Invoice.objects.filter(
            Q(patient__pk=self.object.id)
        ).order_by('-created_on')[:10]
        
        return context

    def get_object(self):
        obj = super().get_object()
        obj.last_accessed = timezone.now()
        obj.save()
        return obj

class CreatePatient(LoginRequiredMixin, RevisionMixin,CreateView):
    model = Patient
    form_class = PatientForm

    #def get_form(self):
     #   pass

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user        
        self.object.save()        
        return HttpResponseRedirect(reverse('patient_detail', args=[self.object.id]))

class UpdatePatient(LoginRequiredMixin,RevisionMixin, UpdateView):
    model = Patient
    fields = [
            'first_name', 'last_name', 'date_of_birth', 'email', 'address','address_line_2',
            'county','eircode','email',
            'contact_number', 'GP_name', 'GP_address'
            ]

#############################################################
#       Create Invoice
class CreateInvoice(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm

    def get_context_data(self, **kwargs):
        context= super(CreateInvoice,self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs.get('pk'))
        return context
    
    def form_valid(self,form):
        form.instance.created_by = self.request.user
        form.instance.total_gross_amount = form.instance.procedure.price
        form.instance.total_net_amount = form.instance.total_amount()
        form.instance.services = form.instance.procedure.codename+' '+form.instance.procedure.description
        form.instance.patient = Patient.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(form)

#############################################################
#        Patient Record Actions

class RecordListView(PermissionRequiredMixin,  ListView):
    permission_required = (
        'clinicmanagement.view_record'
         )
    pk_url_kwarg = 'pk_r'
    paginate_by = 20

    def get_queryset(self):
        object_list = Record.objects.filter(
            Q(patient__pk=self.kwargs.get('pk'))
        ).order_by('-date_of_clinic')
        return object_list



class PatientRecordDetailView(PermissionRequiredMixin, DetailView):
    permission_required = (
        'clinicmanagement.view_record'
         )
    model = Record
    pk_url_kwarg = 'pk_r'

    ##add function to print gp letter
    #def some button 
    #use pdf report to generate field

class CreatePatientRecord(RevisionMixin,PermissionRequiredMixin,CreateView):
    permission_required = (
        'clinicmanagement.add_record'
    )
    model = Record    
    form_class = RecordForm
    pk_url_kwarg = 'pk_r'

    def get_context_data(self, **kwargs):
        context= super(CreatePatientRecord,self).get_context_data(**kwargs)
        print(self.request.user.get_all_permissions())

        context['patient'] = Patient.objects.get(id=self.kwargs.get('pk'))
        return context


    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(id=self.kwargs.get('pk'))
        form.instance.age = form.instance.patient.age()
        return super(CreatePatientRecord,self).form_valid(form)

class UpdatePatientRecord(RevisionMixin, PermissionRequiredMixin,UpdateView):
    permission_required = (
        'clinicmanagement.change_record',
    )
    model = Record
    pk_url_kwarg = 'pk_r'

    fields = ['date_of_clinic', 'referral_indication', 'parity',
            'smear','contraception','medical_history','surgical_history','medications','allergies',
            'current_symptoms', 'investigations_to_date','treatments_to_date',
            'examination_today','further_plan',    
            ]

    def get_context_data(self, **kwargs):
        context= super(UpdatePatientRecord,self).get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(id=self.kwargs.get('pk'))
        return context



class PatientRecordSearchResultsView(LoginRequiredMixin, ListView):

    model = Record
    pk_url_kwarg = 'pk_r'


TOP_MARGIN=1.5 *  inch
BOTTOM_MARGIN = 1 * inch


def get_record(request,pk):
    record = get_object_or_404(Record, pk=pk_r)
    buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontsize = 10
    styleH = styles['BodyText']
    styleO = styles['Normal']
    styleO.alignment = 2
    spacer = Spacer(0, 0.25*inch)

    ##data need for report
    name = record.patient.first_name +' '+ record.patient.last_name
    date_of_birth = record.patient.date_of_birth.strftime("%d-%m-%Y")
    date_of_clinic = record.date_of_clinic.strftime("%d-%m-%Y")
    referral_indication = record.referral_indication
    #medical_history = record.medical_history
    #medications = record.medications
    current_symptoms = record.current_symptoms
    investigations_to_date = record.investigations_to_date
    treatments_to_date = record.treatments_to_date
    examination_today = record.examination_today
    further_plan = record.further_plan
    today_date = timezone.now().date().strftime("%d-%m-%Y")
    gp_name = record.patient.GP_name
    gp_address = record.patient.GP_address

    story = []

    #add some flowables
    story.append(Paragraph(gp_name, styleH))
    story.append(Paragraph(gp_address, styleH))
    story.append(Paragraph(today_date, styleO))

    #add spacer
    story.append(spacer)

    re_title = "Re: "+name+"'s DOB: "+ date_of_birth+" visits to my clinic on "+ date_of_clinic


    #add diagnosis
    story.append(Paragraph(re_title, styleH))

    
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin= TOP_MARGIN, bottomMargin=BOTTOM_MARGIN)
    
    doc.build(story)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='hello0.pdf')
