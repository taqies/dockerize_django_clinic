from django.urls import path

from . import views
from .views import PatientListView, CreatePatient, PatientDetailView, PatientRecordDetailView, PatientSearchResultsView,CreatePatientRecord, CreateInvoice,RecordListView,UpdatePatient,UpdatePatientRecord
from invoices.views import PatientInvoiceListView


urlpatterns = [    
    path('patient/<uuid:pk>', PatientDetailView.as_view(), name = 'patient_detail'),
    path('patient/<uuid:pk>/update', UpdatePatient.as_view(), name = 'update_patient'),
    path('patient/<uuid:pk>/record/<uuid:pk_r>', PatientRecordDetailView.as_view(), name= 'patient_record'),
    path('patient/<uuid:pk>/record/<uuid:pk_r>/update', UpdatePatientRecord.as_view(), name = 'update_record'),
    path('', PatientListView.as_view(), name = 'list_patients'),
    path('add', CreatePatient.as_view(), name = 'create_patient'),
    path('patient/<uuid:pk>/record/add', CreatePatientRecord.as_view(), name = 'create_record'),
    path('patient/<uuid:pk>/records', RecordListView.as_view(), name = 'list_records'),
    path('patient/search', PatientSearchResultsView.as_view(), name = 'patient_search_results'),
    path('patient/<uuid:pk>/record/<uuid:pk_r>/print', views.get_record, name='print_record'),
    path('patient/<uuid:pk>/invoices/add', CreateInvoice.as_view(), name='create_invoice'),
    path('patient/<uuid:pk>/invoices',PatientInvoiceListView.as_view(), name="patient_invoice_list"),
]