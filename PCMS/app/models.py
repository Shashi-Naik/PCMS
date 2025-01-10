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


#================================================================================================================================================================================
class SchArtifactUpload(models.Model):  
    SCHID  = models.CharField(max_length=255)
    PROJID = models.CharField(max_length=255)
    ProjectName = models.CharField(max_length=255)
    SchName = models.CharField(max_length=255)
    SCHPDFPath = models.CharField(max_length=255)
    SCHDSNPath = models.CharField(max_length=255)
    SchCreatedOn = models.CharField(max_length=255)
    SchVersion = models.CharField(max_length=255)
    Last_Updated = models.CharField(max_length=255)
    
    def __str__(self):
        return self.SchName
    class Meta:
        db_table = 'tbl_SchArtifactUpload'    



        
									
class EnggBOMUpload(models.Model):  
    SCHID  = models.CharField(max_length=255)
    PROJID = models.CharField(max_length=255)
    SCHEnggBOMPath = models.CharField(max_length=255)
    SchEnggBOMCreatedOn = models.CharField(max_length=255)
    EnggBOMVersionNumber = models.CharField(max_length=255)
    
    def __str__(self):
        return self.SCHID
    class Meta:
        db_table = 'tbl_EnggBOMUpload'    
				

class PCBArtifactUpload(models.Model):
    SCHID = models.CharField(max_length=255)
    PROJID = models.CharField(max_length=255)
    PCBID = models.CharField(max_length=255)
    PCBLegendName = models.CharField(max_length=255)
    PCBNAme = models.CharField(max_length=255)
    PCBCreatedOn = models.CharField(max_length=255)
    PCBGerberPath = models.CharField(max_length=255)
    PCBGerberUploadDatetime = models.CharField(max_length=255)
    PCBPanelGerberPath = models.CharField(max_length=255)
    PCBPanelGerberUploadDateTime = models.CharField(max_length=255)
    PCBPhoto = models.ImageField(upload_to='pcb_photos/')
    
   

    
    def __str__(self):
        return self.PCBID
    class Meta:
        db_table = 'tbl_PCBArtifactUpload'  
        

        								
class PCBOrderDetailsUpload(models.Model):  
    PCBID  = models.CharField(max_length=255)
    PROJID = models.CharField(max_length=255)
    PCBOrderDateTime = models.CharField(max_length=255)
    PCBOrderQuantity = models.CharField(max_length=255)
    PCBVendorID = models.CharField(max_length=255)
    PCBVendorName = models.CharField(max_length=255)
    PCBReceiptDateTime = models.CharField(max_length=255)
    
    def __str__(self):
        return self.PCBID
    class Meta:
        db_table = 'tbl_PCBOrderDetailsUpload'     
        
					

from django.db import models

class MechanicalDrawingUpload(models.Model):
    MECHID = models.CharField(max_length=255)
    PROJID = models.CharField(max_length=255)
    ProjectName = models.CharField(max_length=255)
    MechDrawingName = models.CharField(max_length=255)
    MechStepFileCreatedOn = models.CharField(max_length=255)
    MechStepFilePath = models.FileField(upload_to='mechanical_drawings/')
    MechCADDrawingCreatedOn = models.CharField(max_length=255)
    MechCADDrawingPath = models.CharField(max_length=255)
    MechBOMPath = models.CharField(max_length=255)
    MechBOMCreatedOn = models.CharField(max_length=255)

    def __str__(self):
        return self.MECHID

    class Meta:
        db_table = 'tbl_MechanicalDrawingUpload'



							

class MechBOMUpload(models.Model):  
    MECHID  = models.CharField(max_length=255)
    PROJID = models.CharField(max_length=255)
    ProjectName = models.CharField(max_length=255)
    SlNo = models.CharField(max_length=255)
    QuantityPerUnit = models.CharField(max_length=255)
    PART  = models.CharField(max_length=255)
    Part_Description = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.MECHID
    class Meta:
        db_table = 'tbl_MechBOMUpload' 











#=====================================================================================================================================================================================        
            
 
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
        db_table = 'tbl_CreateVendor'                 


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
        db_table = 'tbl_CreateCustomer'
        
        


class InternationalCustomers(models.Model):
    customer_name = models.CharField(max_length=100)
    cust_id = models.CharField(max_length=50)
    address = models.TextField()
    type_of_customer = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    aba_routing_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer_name} ({self.cust_id})"
    class Meta:
        db_table = 'tbl_InternationalCustomers_1'
        
class InternationalCustomers2(models.Model):
    customer_name = models.CharField(max_length=100)
    cust_id = models.CharField(max_length=50)
    address = models.TextField()
    type_of_customer = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    aba_routing_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer_name} ({self.cust_id})"
    class Meta:
        db_table = 'tbl_InternationalCustomers_2'        



class CreateProject(models.Model):
    PROJID = models.CharField(max_length= 100)
    CUSTID = models.CharField(max_length=255)
    CustomerName = models.CharField(max_length=255)
    ProjectNAme = models.CharField(max_length=255)
    Description = models.TextField() 
    ProjCodePArtNumberSuffix = models.CharField(max_length=255)
    ProjCodePartNameSuffix = models.CharField(max_length=255)
    FY = models.TextField() 
 
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tbl_CreateProject'







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
    CostPerunit = models.CharField(max_length=255, blank=True, null=True)
    TotalValue = models.CharField(max_length=255, blank=True, null=True)
    Part_number = models.CharField(max_length=255, blank=True, null=True)
    Part_name = models.CharField(max_length=255, blank=True, null=True)
    CGST = models.CharField(max_length=255, blank=True, null=True)
    SGST = models.CharField(max_length=255, blank=True, null=True)
    IGST = models.CharField(max_length=255, blank=True, null=True)
    OptionType = models.CharField(
        max_length=255,
        choices=[
            ('LOCAL', 'LOCAL'),
            ('INTERSTATE', 'INTERSTATE'),
        ]
    )

    def __str__(self):
        return f"Invoice {self.VendorInvoiceNumber} - Project {self.PROJID},HSN[{self.HSN}]"

    class Meta:
        db_table = 'tbl_UploadInvoicefromVendor'





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
        db_table = 'tbl_CreateInvoiceBasedPartNumber'   



#******************************************************************************************************************************************************

class CreatePurchaseBasedCosting(models.Model):
    PROJID = models.CharField(max_length=255,unique=True)
    COSTID = models.CharField(max_length=255)	
    InvoiceValues = models.TextField(max_length=255)	
    PartNums = models.TextField(max_length=255)
    PartNames = models.TextField(max_length=255)	
    Qty	= models.CharField(max_length=255)
    TotalValue = models.CharField(max_length=255)
    	
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tbl_CreatePurchaseBasedCosting'  
        
        
class Costing(models.Model):
    PROJID = models.CharField(max_length=100)
    Project_name = models.CharField(max_length=255)
    Custmer_id = models.CharField(max_length=255)
    Custmer_name = models.CharField(max_length=255)
    InvoiceValues = models.TextField(max_length=255, blank=True)    
    PartNums = models.TextField(max_length=255, blank=True)
    PartNames = models.TextField(max_length=255, blank=True)    
    Qty = models.CharField(max_length=255,blank=True)
    TotalValue = models.CharField(max_length=255,blank=True)
    HSN = models.CharField(max_length=255,blank=True)
    GSTRate = models.CharField(max_length=255)
    CostPerunit = models.CharField(max_length=255, blank=True)
    
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tbl_costing'          
                
        


#******************************************************************************************************************************************************        
class ReadPurchaseBasedCosting(models.Model):
    PROJID = models.CharField(max_length=255)
    COSTID = models.CharField(max_length=255)	
    TotalValue = models.CharField(max_length=255) 	
    CostDetails	= models.CharField(max_length=255)	
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tbl_ReadPurchaseBasedCosting'          
#-----------------------------------------




class GSTR2B(models.Model):
    gstin_supplier = models.CharField(max_length=50, verbose_name="GSTIN of Supplier")
    trade_name = models.CharField(max_length=255, verbose_name="Trade/Legal Name")
    invoice_number = models.CharField(max_length=100)
    invoice_type = models.CharField(max_length=50)
    invoice_date = models.DateField()
    invoice_value = models.DecimalField(max_digits=12, decimal_places=2)
    place_of_supply = models.CharField(max_length=100)
    supply_reverse_charge = models.CharField(max_length=10, verbose_name="Supply Attract Reverse Charge")
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    taxable_value = models.DecimalField(max_digits=12, decimal_places=2)
    integrated_tax = models.DecimalField(max_digits=12, decimal_places=2)
    central_tax = models.DecimalField(max_digits=12, decimal_places=2)
    state_ut_tax = models.DecimalField(max_digits=12, decimal_places=2)
    cess = models.DecimalField(max_digits=12, decimal_places=2)
    gstr_period = models.CharField(max_length=20, verbose_name="GSTR-1/IFF/GSTR-5 Period")
    gstr_filing_date = models.DateField(verbose_name="GSTR-1/IFF/GSTR-5 Filing Date")
    itc_availability = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.gstin_supplier} - {self.invoice_number}"
    class Meta:
        db_table = 'tbl_GSTR2B' 


#=======================================================================================================================



class MechanicalProjectTree(models.Model):
    ProjectID = models.AutoField(primary_key=True)
    ProjectName = models.CharField(max_length=255)
    parentId = models.IntegerField(null=True, blank=True)
    parentName = models.CharField(max_length=255, null=True, blank=True)
    childId = models.IntegerField(null=True, blank=True)
    childName = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ProjectName
    class Meta:
        db_table = 'tbl_MechanicalProjectTree' 
        

        
class MechProject(models.Model):
    ProjectId = models.CharField(max_length=255,null=True)
    ProjectName = models.CharField(max_length=255,null=True)
    ParentId = models.CharField(max_length=255)
    ParentName = models.CharField(max_length=255)
    ChildId = models.CharField(max_length=255)
    ChildName = models.CharField(max_length=255)
    Path = models.CharField(max_length=255)
    DrawingName = models.CharField(max_length=255)
    DrawingId = models.CharField(max_length=255)
    DrawingPath = models.CharField(max_length=255)
    Reamrks = models.CharField(max_length=255,null= True)	
    
    def __str__(self):
        return f"Project ID: {self.ProjectId} - {self.ProjectName}"
    class Meta:
        db_table = 'tbl_MechProject'
        
        
class PCBProject(models.Model):
    ProjectId = models.CharField(max_length=255,null=True)
    ProjectName = models.CharField(max_length=255,null=True)
    ParentId = models.CharField(max_length=255)
    ParentName = models.CharField(max_length=255)
    ChildId = models.CharField(max_length=255)
    ChildName = models.CharField(max_length=255)
    Path = models.CharField(max_length=255)
    PCBName = models.CharField(max_length=255)
    PCBId = models.CharField(max_length=255)
    Reamrks = models.CharField(max_length=255,null= True)	
    
    def __str__(self):
        return f"Project ID: {self.ProjectId} - {self.ProjectName}"
    class Meta:
        db_table = 'tbl_PCBProject'        
        
        
class SCHProject(models.Model):
    ProjectId = models.CharField(max_length=255,null=True)
    ProjectName = models.CharField(max_length=255,null=True)
    ParentId = models.CharField(max_length=255)
    ParentName = models.CharField(max_length=255)
    ChildId = models.CharField(max_length=255)
    ChildName = models.CharField(max_length=255)
    Path = models.CharField(max_length=255)
    SCHName = models.CharField(max_length=255)
    SCHId = models.CharField(max_length=255)
    Reamrks = models.CharField(max_length=255,null= True)	
    
    def __str__(self):
        return f"Project ID: {self.ProjectId} - {self.ProjectName}"
    class Meta:
        db_table = 'tbl_SCHProject'
         
  
    
    
    
           

       
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
        

class CreateVendorStoresInward(models.Model):
    PROJID = models.CharField(max_length=255)
    VENDID = models.CharField(max_length=255)
    VendorInvoiceNumber = models.CharField(max_length=255)
    VendorDCNumber = models.CharField(max_length=255)
    DescriptionofItem = models.CharField(max_length=255)
    QuantityReceived = models.CharField(max_length=255)
    UnitofMEasure = models.CharField(max_length=255)
    BatchID = models.CharField(max_length=255)
    PurchaseORderNumber = models.CharField(max_length=255)
    AcceptedQuantity = models.CharField(max_length=255)
    RejectedQuantity = models.CharField(max_length=255)
    Remarks = models.CharField(max_length=255)
    Receivedby = models.CharField(max_length=255)
    LocationinStore = models.CharField(max_length=255)
    
    def __str__(self):
        return self.PROJID
    class Meta:
        db_table = 'tblCreateVendorStoresInward'  
            

        								
														
       
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