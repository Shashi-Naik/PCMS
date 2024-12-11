
from django import forms
from .models import tblProject,CreateVendor
from .models import tblVendordetails 


class UploadFileForm(forms.Form):
    file = forms.FileField()


from .models import tblPartNumber

class tblPartNumberForm(forms.ModelForm):
    class Meta:
        model = tblPartNumber
        fields = '__all__'
        
        
class vendordetailsForm(forms.ModelForm):
    class Meta:
        model = tblVendordetails  # Use the correct model name here
        fields = ['vendor_name', 'vendor_code', 'gstin', 'address', 'Pan_details', 'Tally_ledger_creation']
# ------------------------------ project testing-----------

# forms.py

class ProjectForm(forms.ModelForm):
    class Meta:
        model = tblProject
        fields = [
            'company_name', 'project_name', 
            'project_code',
        ]

from django import forms
from .models import CreateVendor,CreateCustomer,CreateProject,UploadInvoicefromVendor,CreateInvoiceBasedPartNumber,CreatePurchaseBasedCosting
from .models import ReadPurchaseBasedCosting
class CreateVendorForm(forms.ModelForm):
    class Meta:
        model = CreateVendor
        fields = ['VENDID', 'VendorNAme', 'VEndorGSTIN', 'VendorAddress', 'TypeofVendor', 'BankAcc', 'IFSC', 'Branch']


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = CreateCustomer
        fields = ['CUSTID', 'CustomerName', 'CustomerGSTIN', 'CustomerADdress', 'TypeofCustomer','BankAcc', 'IFSC', 'Branch']


from django import forms
from .models import InternationalCustomers

class InternationalCustomersForm(forms.ModelForm):
    class Meta:
        model = InternationalCustomers
        fields = ['customer_name', 'cust_id', 'address', 'type_of_customer','account_number','swift_code', 'branch', 'aba_routing_code']

from django import forms
from .models import InternationalCustomers2

class InternationalCustomersForm2(forms.ModelForm):
    class Meta:
        model = InternationalCustomers2
        fields = ['customer_name', 'cust_id', 'address', 'type_of_customer','account_number','swift_code', 'branch', 'aba_routing_code']        
        
        
        
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = CreateProject
        fields = ['PROJID', 'CUSTID','CustomerName', 'ProjectNAme', 'Description', 'ProjCodePArtNumberSuffix', 'ProjCodePartNameSuffix','FY']



# from django import forms
# from .models import UploadInvoicefromVendor, CreateProject

# class UploadInvoicefromVendorForm(forms.ModelForm):
#     PROJID = forms.ModelChoiceField(
#         queryset=CreateProject.objects.all(),
#         to_field_name="PROJID",  # This specifies that the value should be the PROJID
#         empty_label="Select"
#     )
#     VENDID = forms.ModelChoiceField(
#         queryset= CreateVendor.objects.all(),
#         to_field_name= "VENDID" ,
#         empty_label="Select"
#     )
    

#     class Meta:
#         model = UploadInvoicefromVendor
#         fields = [
#             'PROJID', 'VENDID', 'VendorInvoiceNumber', 'VendorNAme', 'DateofInvoice', 
#             'UnitOfMeasure', 'QtyReceived', 'GSTRate', 'InvoiceValue', 'HSN'
#         ]


from django import forms
from .models import UploadInvoicefromVendor, CreateProject, CreateVendor

class UploadInvoicefromVendorForm(forms.ModelForm):
    PROJID = forms.ModelChoiceField(
        queryset=CreateProject.objects.all(),
        to_field_name="PROJID",
        empty_label="Select"
    )
    VENDID = forms.ModelChoiceField(
        queryset=CreateVendor.objects.all(),
        to_field_name="VENDID",
        empty_label="Select"
    )
    OptionType = forms.ChoiceField(
        choices=[('LOCAL', 'LOCAL'), ('INTERSTATE', 'INTERSTATE')],
        required=True,
        label="Option Type"
    )

    class Meta:
        model = UploadInvoicefromVendor
        fields = [
            'PROJID', 'VENDID', 'VendorInvoiceNumber', 'VendorNAme', 'DateofInvoice',
            'UnitOfMeasure', 'QtyReceived', 'GSTRate', 'InvoiceValue', 'HSN', 'OptionType'
        ]



class CreateInvoiceBasedPartNumberForm(forms.ModelForm):
    class Meta:
        model = CreateInvoiceBasedPartNumber
        fields = ['PROJID','VENDID','VendorInvoiceNumber','YearOfInvoice','InvoicePartNumber','BAtchID']
        
# class CreatePurchaseBasedCostingForm(forms.ModelForm):
#     PROJID = forms.ModelChoiceField(
#         queryset=UploadInvoicefromVendor.objects.values_list('PROJID', flat=True).distinct(),
#         empty_label="Select"
#     )

#     class Meta:
#         model = CreatePurchaseBasedCosting
#         fields = ['PROJID']





#******************************************************************************************************************************************************
from django import forms
from .models import CreatePurchaseBasedCosting

class CreatePurchaseBasedCostingForm(forms.ModelForm):
    PROJID = forms.ChoiceField(
        label="Project ID",
        required=True
    )

    class Meta:
        model = CreatePurchaseBasedCosting
        fields = ['PROJID', 'COSTID']





# from django import forms
# from .models import Costing

# class CostingForm(forms.ModelForm):
#     PROJID = forms.ChoiceField(
#         label="Project ID",
#         required=True
#     )

#     class Meta:
#         model = CreatePurchaseBasedCosting
#         fields = ['PROJID', 'Project_name','Custmer_id','Custmer_name','InvoiceValues','PartNums','PartNames','Qty','TotalValue','HSN']




#**************************************************************************************************************************************************************************8
from django import forms
from .models import ReadPurchaseBasedCosting, UploadInvoicefromVendor

class ReadPurchaseBasedCostingForm(forms.ModelForm):
    PROJID = forms.ChoiceField(
        label="Project ID",
        required=True
    )

    class Meta:
        model = CreatePurchaseBasedCosting
        fields = ['PROJID']


# class ReadPurchaseBasedCostingForm(forms.ModelForm):
#     PROJID = forms.ChoiceField(
#         choices=[(proj_id, proj_id) for proj_id in UploadInvoicefromVendor.objects.values_list('PROJID', flat=True).distinct()],
#         label="Project ID",
#         required=True
#     )
#     class Meta:
#         model = ReadPurchaseBasedCosting
#         fields = ['PROJID']   

#======================================================================================================================================================================================================================================================================================
from .models import SchArtifactUpload,EnggBOMUpload,PCBArtifactUpload,PCBOrderDetailsUpload,MechanicalDrawingUpload,MechBOMUpload

class SchArtifactUploadForm(forms.ModelForm):
    class Meta:
        model = SchArtifactUpload
        fields = ['SCHID', 'PROJID', 'SchName', 'SCHPDFPath', 'SCHDSNPath', 'SchCreatedOn', 'SchVersion','Last_Updated']
    

#======================================================================================================================================================================================================================================================================================


from django import forms
from .models import EnggBOMUpload

class EnggBOMUploadForm(forms.ModelForm):
    class Meta:
        model = EnggBOMUpload
        fields = ['SCHID', 'PROJID', 'SCHEnggBOMPath', 'SchEnggBOMCreatedOn', 'EnggBOMVersionNumber']



#======================================================================================================================================================================================================================================================================================
from django import forms
from .models import PCBArtifactUpload

class PCBArtifactUploadForm(forms.ModelForm):
    class Meta:
        model = PCBArtifactUpload
        fields = ['SCHID', 'PROJID', 'PCBID', 'PCBLegendName', 'PCBNAme', 'PCBCreatedOn', 'PCBGerberPath', 
                  'PCBGerberUploadDatetime', 'PCBPanelGerberPath', 'PCBPanelGerberUploadDateTime', 'PCBPhoto']



#======================================================================================================================================================================================================================================================================================
class PCBOrderDetailsUploadForm(forms.ModelForm):
    class Meta:
        model = PCBOrderDetailsUpload
        fields = ['PCBID','PROJID','PCBOrderDateTime','PCBOrderQuantity','PCBVendorID','PCBVendorName','PCBReceiptDateTime']

#======================================================================================================================================================================================================================================================================================
from django import forms
from .models import MechanicalDrawingUpload

class MechanicalDrawingUploadForm(forms.ModelForm):
    class Meta:
        model = MechanicalDrawingUpload
        fields = [
            'MECHID', 'PROJID', 'MechDrawingName', 'MechStepFileCreatedOn',
            'MechStepFilePath', 'MechCADDrawingCreatedOn', 'MechCADDrawingPath',
            'MechBOMPath', 'MechBOMCreatedOn'
        ]

#============================================================================================================================
from django import forms
from .models import MechBOMUpload

class MechBOMUploadForm(forms.ModelForm):
    class Meta:
        model = MechBOMUpload
        fields = ['MECHID', 'PROJID', 'SlNo', 'QuantityPerUnit', 'PART', 'Part_Description']
        


#======================================================================================================================================================================================================================================================================================




#======================================================================================================================================================================================================================================================================================






#======================================================================================================================================================================================================================================================================================














