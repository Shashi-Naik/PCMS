from django.urls import path
from . import views
from .views import bulk_update_view, tblProject_view

urlpatterns = [
    path('bulk_update/', bulk_update_view, name='bulk_update_view'),
    path('Project/', tblProject_view, name='tblProject'),
    path('part-number/', views.part_number_view, name='tblPartNumber'),
    path('', views.Vendordetails, name='Vendordetails'),
    #--------------------------------------------------
    path('CreateVendor/', views.CreateVendor_view, name='CreateVendor'),
    path('CreateCustomer/', views.CreateCustomer_view, name='CreateCustomer'),
    path('CreateProject/', views.CreateProject_view, name='CreateProject'),
    path('UploadInvoicefromVendor/', views.UploadInvoicefromVendor_view, name='UploadInvoicefromVendor'),
    path('CreateInvoiceBasedPartNumber/', views.CreateInvoiceBasedPartNumber_view, name='CreateInvoiceBasedPartNumber'),
    path('CreatePurchaseBasedCosting/', views.CreatePurchaseBasedCosting_view, name='CreatePurchaseBasedCosting'),
    path('ReadPurchaseBasedCosting/', views.ReadPurchaseBasedCosting_view, name='ReadPurchaseBasedCosting'),
    
   
]


