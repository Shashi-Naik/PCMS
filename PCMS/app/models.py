# from django.db import models

# class tblProject(models.Model):
#     company_name = models.CharField(max_length=255)
#     company_code = models.CharField(max_length=100)
#     project_name1 = models.CharField(max_length=255)
#     project_code1 = models.CharField(max_length=100)
#     projcode_partnumber = models.CharField(max_length=100)
#     projcode_partname = models.CharField(max_length=255)

#     def __str__(self):
#         return self.project_name1
    
#     class Meta:
#         db_table = 'tblProject'    
        
                
                   
            
        
# from django.db import models

# class tblProject(models.Model):
#     company_name = models.CharField(max_length=255)
#     company_code = models.CharField(max_length=100, blank=True, unique=True)
#     project_name1 = models.CharField(max_length=255)
#     project_code1 = models.CharField(max_length=100)
#     projcode_partnumber = models.CharField(max_length=100)
#     projcode_partname = models.CharField(max_length=255)

#     def __str__(self):
#         return self.project_name1

#     def save(self, *args, **kwargs):
#         if not self.company_code:
            
#             # Check if there's an existing company_code for the same company_name
#             existing_company = tblProject.objects.filter(company_name=self.company_name).first()
        
#             if existing_company:
#                 self.company_code = existing_company.company_code
#             else:
#                 # Generate a new code by finding the maximum existing code and incrementing it
#                 last_code_entry = tblProject.objects.order_by('-company_code').first()
#                 if last_code_entry and last_code_entry.company_code.isdigit():
#                     last_code = int(last_code_entry.company_code)
#                     new_code = last_code + 1
#                 else:
#                     new_code = 1111
#                 self.company_code = str(new_code)
        
#         super().save(*args, **kwargs)
        
#     class Meta:
#         db_table = 'tblProject'
from django.db import models

class tblProject(models.Model):
    company_name = models.CharField(max_length=255)
    company_code = models.CharField(max_length=100, blank=True, unique=True)
    project_name = models.CharField(max_length=255)
    project_code = models.CharField(max_length=100)
    projcode_partnumber = models.CharField(max_length=100, blank=True)
    projcode_partname = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name1

    def save(self, *args, **kwargs):
        if not self.company_code:
            # Check if there's an existing company_code for the same company_name
            existing_company = tblProject.objects.filter(company_name=self.company_name).first()
            if existing_company:
                self.company_code = existing_company.company_code
            else:
                # Generate a new company_code by finding the highest existing code and incrementing it
                last_code_entry = tblProject.objects.order_by('-company_code').first()
                if last_code_entry and last_code_entry.company_code.isdigit():
                    last_code = int(last_code_entry.company_code)
                    new_code = last_code + 1
                else:
                    new_code = 1111
                self.company_code = str(new_code)

        # Generate projcode_partnumber based on company_code
        if not self.projcode_partnumber:
           
            same_code_count = tblProject.objects.filter(company_code=self.company_code).count() + 1
            self.projcode_partnumber = f"{self.company_code}_{same_code_count}"
            
       
            self.projcode_partname = f"{self.company_name}_{self.projcode_partnumber}"

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tblProject'



class tblVendordetails(models.Model):
    vendor_name = models.CharField(max_length=255)
    vendor_code = models.CharField(max_length=100, blank=True, null=True, unique=True)  # Allowing blank values
    gstin = models.CharField(max_length=15)
    address = models.TextField()
    Pan_details = models.CharField(max_length=255)
    Tally_ledger_creation = models.CharField(max_length=255)


    def __str__(self):
        return self.vendor_name


class tblPartNumber(models.Model):
    part_number = models.CharField(max_length=100)
    part_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    hsn = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=100)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2)  
    date_of_invoice = models.DateField()
    uqc = models.CharField(max_length=50) 
    invoice_value = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=10, decimal_places=2)  
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_invoice = models.DecimalField(max_digits=15, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    paid_date = models.DateField(null=True, blank=True)
    paid_by = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100)
    gstr2b = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    ledger = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.part_number
    
    class Meta:
        db_table = 'tblPartNumber'  
        