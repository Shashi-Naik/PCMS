from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


from .models import tblPartNumber

class tblPartNumberForm(forms.ModelForm):
    class Meta:
        model = tblPartNumber
        fields = '__all__'

# ------------------------------
# from django import forms
# from .models import tblVendordetails

# class VendorForm(forms.ModelForm):
#     class Meta:
#         model = tblVendordetails
#         fields = '__all__'
