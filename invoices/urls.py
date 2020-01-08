from . import views
from django.urls import path
from .views import InvoiceListView, DetailInvoice

urlpatterns = [
    path('', InvoiceListView.as_view()),    
    path('<int:pk>', DetailInvoice.as_view(), name='invoice_detail'),
    path('<int:pk>/print', views.print_invoice,name='print_invoice')
]