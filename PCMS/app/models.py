from django.db import models

class tblProject(models.Model):
    company_name = models.CharField(max_length=255)
    company_code = models.CharField(max_length=100)
    project_name1 = models.CharField(max_length=255)
    project_code1 = models.CharField(max_length=100)
    projcode_partnumber = models.CharField(max_length=100)
    projcode_partname = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name1
    
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
        