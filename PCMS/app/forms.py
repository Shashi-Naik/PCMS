from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


from .models import tblPartNumber

class tblPartNumberForm(forms.ModelForm):
    class Meta:
        model = tblPartNumber
        fields = '__all__'

# ------------------------------ project testing-----------

# forms.py
from django import forms
from .models import tblProject

class ProjectForm(forms.ModelForm):
    class Meta:
        model = tblProject
        fields = [
            'company_name', 'project_name1', 
            'project_code1', 'projcode_partnumber', 'projcode_partname'
        ]




