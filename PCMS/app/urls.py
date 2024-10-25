from django.urls import path
from . import views
from .views import bulk_update_view, tblProject_view

urlpatterns = [
    path('bulk_update/', bulk_update_view, name='bulk_update_view'),
    path('Project/', tblProject_view, name='tblProject'),
    path('part-number/', views.part_number_view, name='tblPartNumber'),
    path('Vendordetails/', views.Vendordetails, name='Vendordetails'),# Added a comma here after tblProject_view
]


# ------------------------------------
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.vendor_list, name='vendor_list'),
#     path('new/', views.vendor_create, name='vendor_create'),
#     path('edit/<int:pk>/', views.vendor_update, name='vendor_update'),
#     path('delete/<int:pk>/', views.vendor_delete, name='vendor_delete'),
#     path('upload/', views.vendor_upload, name='vendor_upload'),
# ]
