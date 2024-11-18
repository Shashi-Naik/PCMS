
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
        
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = CreateProject
        fields = ['PROJID', 'CUSTID', 'ProjectNAme', 'Description', 'ProjCodePArtNumberSuffix', 'ProjCodePartNameSuffix','FY']



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
        
class CreatePurchaseBasedCostingForm(forms.ModelForm):
    class Meta:
        model = CreatePurchaseBasedCosting
        fields = ['PROJID','COSTID','InvoicePartNumber','CostPerUnit','Qty','TotalValue']        



class ReadPurchaseBasedCostingForm(forms.ModelForm):
    class Meta:
        model = ReadPurchaseBasedCosting
        fields = ['PROJID','COSTID','TotalValue','CostDetails']   
















