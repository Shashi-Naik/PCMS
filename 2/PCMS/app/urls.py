from django.urls import path
from . import views
from .views import bulk_update_view, tblProject_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('bulk_update/', bulk_update_view, name='bulk_update_view'),
    path('Project/', tblProject_view, name='tblProject'),
    path('part-number/', views.part_number_view, name='tblPartNumber'),
    path('', views.Vendordetails, name='Vendordetails'),
    #--------------------------------------------------
    path('CreateVendor/', views.CreateVendor_view, name='CreateVendor'),
    path('CreateCustomer/', views.CreateCustomer_view, name='CreateCustomer'),
    path('international_vendor/', views.international_customer_view, name='international_customer'),
    path('international_customer/', views.international_customer_2, name='international_customer_2'),
    
    path('CreateProject/', views.CreateProject_view, name='CreateProject'),
    path('UploadInvoicefromVendor/', views.UploadInvoicefromVendor_view, name='UploadInvoicefromVendor'),
    path('CreateInvoiceBasedPartNumber/', views.CreateInvoiceBasedPartNumber_view, name='CreateInvoiceBasedPartNumber'),
    path('CreatePurchaseBasedCosting/', views.CreatePurchaseBasedCosting_view, name='CreatePurchaseBasedCosting'),
    path('ReadPurchaseBasedCosting/', views.ReadPurchaseBasedCosting_view, name='ReadPurchaseBasedCosting'),
    
    path('SchArtifactUpload/', views.SchArtifactUpload_view, name='SchArtifactUpload'),
    path('engg_bom_upload/', views.engg_bom_upload_view, name='engg_bom_upload'),
    path('pcbartifactupload/', views.pcbartifactupload_view, name='pcbartifactupload_view'),
    path('PCBOrderDetailsUpload/', views.PCBOrderDetailsUpload_view, name='PCBOrderDetailsUpload'),
    path('mechanical_drawing/', views.MechanicalDrawingUpload_view, name='MechanicalDrawingUpload'),
    path('MechBOMUpload/', views.MechBOMUpload_view, name='MechBOMUpload'),
    
    
    path('costing/', views.project_dropdown_view, name='select_project'),
    path('qutation/', views.qutation, name='qutation'),
    
    
    path('gstr2b/', views.bulk_insert_gstr2b, name='gstr2b'),
    
    
    
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



