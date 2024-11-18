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
        return self.project_name

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
    vendor_code = models.CharField(max_length=100, blank=True, null=True, unique=True)  
    gstin = models.CharField(max_length=15,null=True)
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
        
        
        
#------------------------------------------------------------------------------------------------------------------------------

class CreateVendor(models.Model):
    VENDID = models.CharField(max_length=255, unique=True)
    VendorNAme = models.CharField(max_length=255)
    VEndorGSTIN = models.CharField(max_length=15, unique=True)
    VendorAddress = models.TextField()
    VendorPAN = models.CharField(max_length=255, blank=True)
    TypeofVendor = models.CharField(max_length=100)
    BankAcc = models.CharField(max_length=100)
    IFSC = models.CharField(max_length=100)
    Branch = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Auto-generate VendorPAN based on VEndorGSTIN
        if self.VEndorGSTIN and len(self.VEndorGSTIN) >= 15:
            self.VendorPAN = self.VEndorGSTIN[2:-3]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.VENDID

    class Meta:
        db_table = 'tblCreateVendor'

        
            
                  


class CreateCustomer(models.Model):
    CUSTID =models.CharField(max_length= 100)
    CustomerName = models.CharField(max_length=255)
    CustomerGSTIN = models.CharField(max_length=15,unique=True)
    CustomerADdress = models.TextField() 
    CustomerPAN = models.CharField(max_length=255)
    TypeofCustomer = models.CharField(max_length=100) 
    BankAcc = models.CharField(max_length=100)
    IFSC = models.CharField(max_length=100)
    Branch = models.CharField(max_length=100)
    
    def save(self,*args, **kwargs):
        if self.CustomerGSTIN and len(self.CustomerGSTIN) >= 15:
            self.CustomerPAN = self.CustomerGSTIN[2:-3]
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.CustomerName
    class Meta:
        db_table = 'tblCreateCustomer'




class CreateProject(models.Model):
    PROJID = models.CharField(max_length= 100)
    CUSTID = models.CharField(max_length=255)
    ProjectNAme = models.CharField(max_length=255)
    Description = models.TextField() 
    ProjCodePArtNumberSuffix = models.CharField(max_length=255)
    ProjCodePartNameSuffix = models.CharField(max_length=255)
    FY = models.TextField() 
 
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tblCreateProject'





# from django.db import models
# from decimal import Decimal, InvalidOperation
# from django.core.exceptions import ValidationError
# from decimal import Decimal, InvalidOperation
# from django.db import models
# from django.core.exceptions import ValidationError

# class UploadInvoicefromVendor(models.Model):
#     PROJID = models.CharField(max_length=255)
#     VENDID = models.CharField(max_length=255)
#     VendorInvoiceNumber = models.CharField(max_length=255)
#     VendorNAme = models.CharField(max_length=255)
#     DateofInvoice = models.CharField(max_length=255)
#     UnitOfMeasure = models.CharField(max_length=255)
#     QtyReceived = models.CharField(max_length=255)
#     GSTRate = models.CharField(max_length=255)
#     InvoiceValue = models.CharField(max_length=255)
#     HSN = models.CharField(max_length=255)
#     CostPerunit = models.CharField(max_length=255, blank=True)
#     TotalValue = models.CharField(max_length=255, blank=True)  # Initially blank
#     Part_number = models.CharField(max_length=255, blank=True)  # Can be blank initially
#     Part_name = models.CharField(max_length=255, blank=True)

#     def save(self, *args, **kwargs):
#         # Retrieve FY, ProjCodePArtNumberSuffix, and ProjCodePartNameSuffix from the related CreateProject instance
#         try:
#             project = CreateProject.objects.get(PROJID=self.PROJID)
#             # Generate Part_number
#             self.Part_number = f"{project.FY}-{project.ProjCodePArtNumberSuffix}-{self.VENDID}-{self.VendorInvoiceNumber}"
#             # Generate Part_name
#             self.Part_name = f"{project.FY}-{project.ProjCodePartNameSuffix}-{self.VENDID}-{self.VendorInvoiceNumber}"
#         except CreateProject.DoesNotExist:
#             # Handle case if the project does not exist (optional)
#             self.Part_number = "Invalid Project ID"
#             self.Part_name = "Invalid Project Name"

#         # Calculate CostPerunit
#         try:
#             invoice_value = float(self.InvoiceValue)
#             qty_received = float(self.QtyReceived)
#             self.CostPerunit = "{:.2f}".format(invoice_value / qty_received)
#         except (ValueError, ZeroDivisionError) as e:
#             self.CostPerunit = "Error in calculation"

#         # Calculate TotalValue
#         try:
#             invoice_value = float(self.InvoiceValue)
#             gst_rate = float(self.GSTRate.strip('%')) / 100
#             self.TotalValue = "{:.2f}".format(invoice_value * (1 + gst_rate))
#         except ValueError as e:
#             self.TotalValue = "Error in calculation"

#         super().save(*args, **kwargs)  # Save the instance with the generated values

#     def __str__(self):
#         return self.PROJID

#     class Meta:
#         db_table = 'tblUploadInvoicefromVendor'


from django.db import models

class UploadInvoicefromVendor(models.Model):
    PROJID = models.CharField(max_length=255)
    VENDID = models.CharField(max_length=255)
    VendorInvoiceNumber = models.CharField(max_length=255)
    VendorNAme = models.CharField(max_length=255)
    DateofInvoice = models.CharField(max_length=255)
    UnitOfMeasure = models.CharField(max_length=255)
    QtyReceived = models.CharField(max_length=255)
    GSTRate = models.CharField(max_length=255)
    InvoiceValue = models.CharField(max_length=255)
    HSN = models.CharField(max_length=255)
    CostPerunit = models.CharField(max_length=255, blank=True)
    TotalValue = models.CharField(max_length=255, blank=True)
    Part_number = models.CharField(max_length=255, blank=True)
    Part_name = models.CharField(max_length=255, blank=True)
    CGST = models.CharField(max_length=255, blank=True)
    SGST = models.CharField(max_length=255, blank=True)
    IGST = models.CharField(max_length=255, blank=True)
    OptionType = models.CharField(max_length=255, choices=[('LOCAL', 'LOCAL'), ('INTERSTATE', 'INTERSTATE')])

    def save(self, *args, **kwargs):
        try:
            project = CreateProject.objects.get(PROJID=self.PROJID)
            self.Part_number = f"{project.FY}-{project.ProjCodePArtNumberSuffix}-{self.VENDID}-{self.VendorInvoiceNumber}"
            self.Part_name = f"{project.FY}-{project.ProjCodePartNameSuffix}-{self.VENDID}-{self.VendorInvoiceNumber}"
        except CreateProject.DoesNotExist:
            self.Part_number = "Invalid Project ID"
            self.Part_name = "Invalid Project Name"

        try:
            invoice_value = float(self.InvoiceValue)
            qty_received = float(self.QtyReceived)
            self.CostPerunit = "{:.2f}".format(invoice_value / qty_received)
        except (ValueError, ZeroDivisionError):
            self.CostPerunit = "Error in calculation"

        try:
            invoice_value = float(self.InvoiceValue)
            gst_rate = float(self.GSTRate.strip('%')) / 100
            self.TotalValue = "{:.2f}".format(invoice_value * (1 + gst_rate))
        except ValueError:
            self.TotalValue = "Error in calculation"

        try:
            invoice_value = float(self.InvoiceValue)
            gst_rate = float(self.GSTRate.strip('%'))/100
            print(gst_rate)
            if self.OptionType == 'LOCAL':
                self.CGST = invoice_value * gst_rate / 2
                self.SGST = invoice_value * gst_rate / 2
                self.IGST = "0"
            elif self.OptionType == 'INTERSTATE':
                self.CGST = "0"
                self.SGST = "0"
                self.IGST = invoice_value * gst_rate / 1
        except ValueError:
            self.CGST = self.SGST = self.IGST = "Error in calculation"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.PROJID

    class Meta:
        db_table = 'tblUploadInvoicefromVendor'



class CreateInvoiceBasedPartNumber(models.Model):
    PROJID = models.CharField(max_length=255)
    VENDID = models.CharField(max_length=255)	
    VendorInvoiceNumber = models.CharField(max_length=255)
    YearOfInvoice = models.CharField(max_length=255)
    InvoicePartNumber = models.CharField(max_length=255)
    BAtchID = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tblCreateInvoiceBasedPartNumber'   




class CreatePurchaseBasedCosting(models.Model):
    PROJID = models.CharField(max_length=255)
    COSTID = models.CharField(max_length=255)	
    InvoicePartNumber = models.CharField(max_length=255)	
    CostPerUnit = models.CharField(max_length=255)	
    Qty	= models.CharField(max_length=255)
    TotalValue = models.CharField(max_length=255)	
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tblCreatePurchaseBasedCosting'  
        
        
        
        
class ReadPurchaseBasedCosting(models.Model):
    PROJID = models.CharField(max_length=255)
    COSTID = models.CharField(max_length=255)	
    TotalValue = models.CharField(max_length=255) 	
    CostDetails	= models.CharField(max_length=255)	
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tblReadPurchaseBasedCosting'          
#-----------------------------------------

       
# class CreateProject(models.Model):
#     PROJID = models.CharField(max_length= 100)
#     CUSTID = models.CharField(max_length=255)
#     ProjectNAme = models.CharField(max_length=255)
#     Description = models.TextField() 
#     ProjCodePArtNumberSuffix = models.CharField(max_length=255)
#     ProjCodePartNameSuffix = models.CharField(max_length=255)
#     FY = models.TextField() 
 
#     def __str__(self):
#         return self.ProjectNAme
#     class Meta:
#         db_table = 'tblCreateProject'
        

# class CreatePurchaseBatch(models.Model):
#     SCHID = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
#     BatchName = models.CharField(max_length=255)
#     CustomerID = models.CharField(max_length=255)
#     CustomerName = models.CharField(max_length=255)
#     CustomerPONumber = models.CharField(max_length=255)
#     CustomerPODate = models.CharField(max_length=255)
#     CustomerQuantity = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.BatchName
#     class Meta:
#         db_table = 'tblCreatePurchaseBatch'    
        
														
   
# class PurchaseBOMRFQ(models.Model):
#     SCHID = models.CharField(max_length=255)
#     SlNo = models.IntegerField()
#     QuantityPerUnit = models.CharField(max_length=255)
#     PART = models.CharField(max_length=255)
#     PartDescription = models.CharField(max_length=255)
#     Manufacturer = models.CharField(max_length=255)
#     ManufacturerPartNumber = models.CharField(max_length=255)
#     PurchaseLocal = models.CharField(max_length=255)
#     PurchaseImport = models.CharField(max_length=255)
#     VendorID = models.CharField(max_length=255)
   
#     def __str__(self):
#         return self.SlNo
#     class Meta:
#         db_table = 'tblPurchaseBOMRFQ'    
  
							
        
# class PurchaseBOMtoVendor(models.Model):
#     SCHID = models.CharField(max_length=255)
#     SlNo = models.IntegerField()
#     QuantityPerUnit = models.CharField(max_length=255)
#     PART = models.CharField(max_length=255)
#     PartDescription = models.CharField(max_length=255)
#     TotalQuantity = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.SlNo
#     class Meta:
#         db_table = 'tblPurchaseBOMtoVendor'   
        
				
        
# class UpdateQuotefromVendor(models.Model):
#     SCHID = models.CharField(max_length=255)
#     SlNo = models.IntegerField()
#     QuantityPerUnit = models.CharField(max_length=255)
#     PART = models.CharField(max_length=255)
#     PartDescription = models.CharField(max_length=255)
#     ManufacturerPartNumber = models.CharField(max_length=255)
#     ValuePerUnitINR = models.CharField(max_length=255)
#     TotalValueINR = models.CharField(max_length=255)
#     LeadTime = models.CharField(max_length=255)
#     VendorID = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.SlNo
#     class Meta:
#         db_table = 'tblUpdateQuotefromVendorr'  
        


# class CompareVendorQuotes(models.Model):
#     SCHID = models.CharField(max_length=255)
#     SlNo = models.IntegerField()
#     QuantityPerUnit = models.CharField(max_length=255)
#     PART = models.CharField(max_length=255)
#     PartDescription = models.CharField(max_length=255)
#     ManufacturerPartNumber = models.CharField(max_length=255)
#     ValuePerUnitINR = models.CharField(max_length=255)
#     TotalValueINR = models.CharField(max_length=255)
#     TotalQuantity = models.CharField(max_length=255)
#     LeadTime = models.CharField(max_length=255)
#     VendorID = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.SlNo
#     class Meta:
#         db_table = 'tblCompareVendorQuotes'  
        
	

# class IssuePOToVendor(models.Model):
#     SCHID = models.CharField(max_length=255)
#     SlNo = models.IntegerField()
#     PART = models.CharField(max_length=255)
#     PartDescription = models.CharField(max_length=255)
#     ManufacturerPartNumber = models.CharField(max_length=255)
#     TotalQuantity = models.CharField(max_length=255)
#     TotalValueINR = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
#     PONumber = models.CharField(max_length=255)
#     PODate = models.CharField(max_length=255)
   
#     def __str__(self):
#         return self.SlNo
#     class Meta:
#         db_table = 'tblIssuePOToVendor'  
        
									
# class UploadInvoicefromVendor(models.Model):
#     PROJID = models.CharField(max_length=255)
#     VENDID = models.CharField(max_length=255)	
#     VendorInvoiceNumber = models.CharField(max_length=255)
#     VendorNAme = models.CharField(max_length=255)
#     DateofInvoice = models.CharField(max_length=255)
#     UnitOfMeasure = models.CharField(max_length=255)
#     QtyReceived = models.CharField(max_length=255)
#     GSTRate = models.CharField(max_length=255)
#     HSN = models.CharField(max_length=255)
#     CostPerunit = models.CharField(max_length=255)
#     TotalValue = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblUploadInvoicefromVendor'  

						

# class CreateInvoiceBasedPartNumber(models.Model):
#     PROJID = models.CharField(max_length=255)
#     VENDID = models.CharField(max_length=255)	
#     VendorInvoiceNumber = models.CharField(max_length=255)
#     YearOfInvoice = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     BAtchID = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateInvoiceBasedPartNumber'   
        
							
# class CreatePurchaseBasedCosting(models.Model):
#     PROJID = models.CharField(max_length=255)
#     COSTID = models.CharField(max_length=255)	
#     InvoicePartNumber = models.CharField(max_length=255)	
#     CostPerUnit = models.CharField(max_length=255)	
#     Qty	= models.CharField(max_length=255)
#     TotalValue = models.CharField(max_length=255)	
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreatePurchaseBasedCosting'  
        
	
# class ReadPurchaseBasedCosting(models.Model):
#     PROJID = models.CharField(max_length=255)
#     COSTID = models.CharField(max_length=255)	
#     TotalValue = models.CharField(max_length=255) 	
#     CostDetails	= models.CharField(max_length=255)	
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblReadPurchaseBasedCosting'  
        

# class CreateVendorStoresInward(models.Model):
#     PROJID = models.CharField(max_length=255)
#     VENDID = models.CharField(max_length=255)
#     VendorInvoiceNumber = models.CharField(max_length=255)
#     VendorDCNumber = models.CharField(max_length=255)
#     DescriptionofItem = models.CharField(max_length=255)
#     QuantityReceived = models.CharField(max_length=255)
#     UnitofMEasure = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
#     PurchaseORderNumber = models.CharField(max_length=255)
#     AcceptedQuantity = models.CharField(max_length=255)
#     RejectedQuantity = models.CharField(max_length=255)
#     Remarks = models.CharField(max_length=255)
#     Receivedby = models.CharField(max_length=255)
#     LocationinStore = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateVendorStoresInward'  
            

        								
														
       
# class CreateCustomerStoresInward(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     CUSTID  = models.CharField(max_length=255)
#     CustomerDCNumber = models.CharField(max_length=255)
#     DescriptionofItem = models.CharField(max_length=255)
#     QuantityReceived  = models.CharField(max_length=255)
#     UnitofMEasure  = models.CharField(max_length=255)
#     CauseofInward  = models.CharField(max_length=255)
#     Remarks  = models.CharField(max_length=255)
#     Receivedby  = models.CharField(max_length=255)
#     LocationinStore  = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateCustomerStoresInward'  
    
     
		
# class CreateOthersStoresInward(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     OTHERSID  = models.CharField(max_length=255)
#     OthersDCNumber = models.CharField(max_length=255)
#     DescriptionofItem = models.CharField(max_length=255)
#     QuantityReceived  = models.CharField(max_length=255)
#     UnitofMEasure  = models.CharField(max_length=255)
#     CauseofInward  = models.CharField(max_length=255)
#     Remarks  = models.CharField(max_length=255)
#     Receivedby  = models.CharField(max_length=255)
#     LocationinStore  = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateOthersStoresInward'                                 
                               
                               
							
# class CreateStoresOutwardtoProduction(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     PRODID  = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     Quantity  = models.CharField(max_length=255)
#     TotalValue  = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateStoresOutwardtoProduction'   
        

# class CreateStoresOutwardtoSales(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     BatchID  = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     Quantity  = models.CharField(max_length=255)
#     TotalValue  = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateStoresOutwardtoSales' 
        	
									
# class CreateStoresOutwardtoRnD(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     BatchID  = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     Quantity  = models.CharField(max_length=255)
#     TotalValue  = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateStoresOutwardtoRnD' 
     						
# class CreateStoresOutwardtoRepairs(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     BatchID  = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     Quantity  = models.CharField(max_length=255)
#     TotalValue  = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateStoresOutwardtoRepairs'                 							

	
# class CreateProductionBatch(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     CUSTID = models.CharField(max_length=255)
#     CustomerPONumber = models.CharField(max_length=255)
#     CustomerPODate = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     Quantity = models.CharField(max_length=255)
#     FGName = models.CharField(max_length=255)
#     FGQuantity = models.CharField(max_length=255)
#     TotalValue = models.CharField(max_length=255)
   
    
    
#     def __str__(self):
#         return self.PROJID
#     class Meta:
#         db_table = 'tblCreateProductionBatch'       

								
# class CreateStockJournalforFG(models.Model):  
#     JOURNALID  = models.CharField(max_length=255)
#     BatchID = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     Quantity = models.CharField(max_length=255)
#     TotalValue = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.JOURNALID
#     class Meta:
#         db_table = 'tblCreateStockJournalforFG'        
        
										
# class CreateFinishedGoods(models.Model):  
#     CUSTID  = models.CharField(max_length=255)
#     JOURNALID = models.CharField(max_length=255)
#     FGName = models.CharField(max_length=255)
#     UnitofMeasure = models.CharField(max_length=255)
#     HSN = models.CharField(max_length=255)
#     GST = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.JOURNALID
#     class Meta:
#         db_table = 'tblCreateFinishedGoods'     
						
# class CreateQuotetoCustomer(models.Model):  
#     PROJID  = models.CharField(max_length=255)
#     QUOTEID = models.CharField(max_length=255)
#     InvoicePartNumber = models.CharField(max_length=255)
#     CostPerUnit = models.CharField(max_length=255)
#     Qty = models.CharField(max_length=255)
#     TotalValue = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.QUOTEID
#     class Meta:
#         db_table = 'tblCreateQuotetoCustomer'           				
                                       
# class SchArtifactUpload(models.Model):  
#     SCHID  = models.CharField(max_length=255)
#     SchName = models.CharField(max_length=255)
#     SCHPDFPath = models.CharField(max_length=255)
#     SCHDSNPath = models.CharField(max_length=255)
#     SchCreatedOn = models.CharField(max_length=255)
#     SchVersion = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.SchName
#     class Meta:
#         db_table = 'tblSchArtifactUpload'     
        
									
# class EnggBOMUpload(models.Model):  
#     SCHID  = models.CharField(max_length=255)
#     SCHEnggBOMPath = models.CharField(max_length=255)
#     SchEnggBOMCreatedOn = models.CharField(max_length=255)
#     EnggBOMVersionNumber = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.SCHID
#     class Meta:
#         db_table = 'tblEnggBOMUpload'    
				

# class PCBArtifactUpload(models.Model):
#     SCHID = models.CharField(max_length=255)
#     PCBID = models.CharField(max_length=255)
#     PCBLegendName = models.CharField(max_length=255)
#     PCBNAme = models.CharField(max_length=255)
#     PCBCreatedOn = models.CharField(max_length=255)
#     PCBGerberPath = models.CharField(max_length=255)
#     PCBGerberUploadDatetime = models.CharField(max_length=255)
#     PCBPanelGerberPath = models.CharField(max_length=255)
#     PCBPanelGerberUploadDateTime = models.CharField(max_length=255)
#     PCBPhoto = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PCBID
#     class Meta:
#         db_table = 'tblPCBArtifactUpload'  
        

        								
# class PCBOrderDetailsUpload(models.Model):  
#     PCBID  = models.CharField(max_length=255)
#     PCBOrderDateTime = models.CharField(max_length=255)
#     PCBOrderQuantity = models.CharField(max_length=255)
#     PCBVendorID = models.CharField(max_length=255)
#     PCBVendorName = models.CharField(max_length=255)
#     PCBReceiptDateTime = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.PCBID
#     class Meta:
#         db_table = 'tblPCBOrderDetailsUpload'     
        
					

# class MechanicalDrawingUpload(models.Model):  
#     MECHID  = models.CharField(max_length=255)
#     MechDrawingNAme = models.CharField(max_length=255)
#     MechStepFileCreatedOn = models.CharField(max_length=255)
#     MechStepFilePath = models.CharField(max_length=255)
#     MechCADDrawingCreatedOn = models.CharField(max_length=255)
#     MechCADDrawingPAth = models.CharField(max_length=255)
#     MechBOMPath = models.CharField(max_length=255)
#     MechBOMCreatedOn = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.MECHID
#     class Meta:
#         db_table = 'tblMechanicalDrawingUpload'      
        

# class QuantityPerUnit(models.Model):  
#     PART  = models.CharField(max_length=255)
#     PartDescription = models.CharField(max_length=255)
    
    
#     def __str__(self):
#         return self.PART
#     class Meta:
#         db_table = 'tblQuantityPerUnit'     								
                                                                            
#  #----------------------------------------------------------------------------------------------------------------------   
    
        
        
#         i have 2 model.py

# class tblPartNumber(models.Model):
#     part_number = models.CharField(max_length=100)
#     part_name = models.CharField(max_length=255)
#     vendor_name = models.CharField(max_length=255)
#     project_name = models.CharField(max_length=255)
#     description = models.TextField()
#     hsn = models.CharField(max_length=50)
#     invoice_number = models.CharField(max_length=100)
#     gst_rate = models.DecimalField(max_digits=5, decimal_places=2)  
#     date_of_invoice = models.DateField()
#     uqc = models.CharField(max_length=50) 
#     invoice_value = models.DecimalField(max_digits=10, decimal_places=2)
#     qty = models.DecimalField(max_digits=10, decimal_places=2)  
#     cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
#     total_invoice = models.DecimalField(max_digits=15, decimal_places=2)
#     payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
#     paid_date = models.DateField(null=True, blank=True)
#     paid_by = models.CharField(max_length=100, null=True, blank=True)
#     type = models.CharField(max_length=100)
#     gstr2b = models.CharField(max_length=100, null=True, blank=True)
#     remarks = models.TextField(null=True, blank=True)
#     ledger = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.part_number
    
#     class Meta:
#         db_table = 'tblPartNumber'  
        
# class UploadInvoicefromVendor(models.Model):
#     PROJID = models.CharField(max_length=255)
#     VENDID = models.CharField(max_length=255)
#     VendorInvoiceNumber = models.CharField(max_length=255)
#     VendorNAme = models.CharField(max_length=255)
#     DateofInvoice = models.CharField(max_length=255)
#     UnitOfMeasure = models.CharField(max_length=255)
#     QtyReceived = models.CharField(max_length=255)
#     GSTRate = models.CharField(max_length=255)
#     InvoiceValue = models.CharField(max_length=255)
#     HSN = models.CharField(max_length=255)
#     CostPerunit = models.CharField(max_length=255, blank=True)
#     TotalValue = models.CharField(max_length=255, blank=True)
#     Part_number = models.CharField(max_length=255, blank=True)
#     Part_name = models.CharField(max_length=255, blank=True)
#     CGST = models.CharField(max_length=255, blank=True)
#     SGST = models.CharField(max_length=255, blank=True)
#     IGST = models.CharField(max_length=255, blank=True)
#     OptionType = models.CharField(max_length=255, choices=[('LOCAL', 'LOCAL'), ('INTERSTATE', 'INTERSTATE')])