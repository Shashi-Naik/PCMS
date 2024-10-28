from django.urls import path
from . import views
from .views import bulk_update_view, tblProject_view

urlpatterns = [
    path('bulk_update/', bulk_update_view, name='bulk_update_view'),
    path('Project/', tblProject_view, name='tblProject'),
    path('part-number/', views.part_number_view, name='tblPartNumber'),
    path('', views.Vendordetails, name='Vendordetails'),
   
]

