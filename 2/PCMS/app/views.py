import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import tblVendordetails, tblProject, tblPartNumber
from django.core.files.storage import FileSystemStorage

# Helper function to safely strip a value if it's a string
def safe_strip(value):
    """Helper function to safely strip a value if it's a string."""
    if isinstance(value, str):
        return value.strip()
    print(value)
    return value  # Return the original value if it's not a string

def bulk_update_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Read the Excel file
                xls = pd.ExcelFile(file)

                # Log the sheet names to ensure they are being read correctly
                sheet_names = xls.sheet_names
                stripped_sheet_names = [name.strip() for name in sheet_names]
                print("Detected sheet names:", stripped_sheet_names)

                # Process sheet 1 - Project (tblProject)
                if any(name.strip() == 'Project' for name in sheet_names):
                    df_project = pd.read_excel(xls, sheet_name=[name for name in sheet_names if name.strip() == 'Project'][0])
                    for _, row in df_project.iterrows():
                        tblProject.objects.update_or_create(
                            company_code=safe_strip(row['Company Code']),  # Assuming company_code is unique
                            defaults={
                                'company_name': safe_strip(row['Company Name']),
                                'project_name': safe_strip(row['Project Name1']),
                                'project_code': safe_strip(row['ProjectCode1']),
                                'projcode_partnumber': safe_strip(row['ProjCode- Partnumber']),
                                'projcode_partname': safe_strip(row['ProjCode-Partname'])
                            }
                        )
                else:
                    raise ValueError("Worksheet named 'Project' not found")

                # Process sheet 2 - Vendor Code (tblVendordetails)
                if any(name.strip() == 'Vendor Code' for name in sheet_names):
                    df_vendor_code = pd.read_excel(xls, sheet_name=[name for name in sheet_names if name.strip() == 'Vendor Code'][0])
                    for _, row in df_vendor_code.iterrows():
                        tblVendordetails.objects.update_or_create(
                            vendor_code=safe_strip(row['Vendor Code']),  # Assuming vendor_code is unique
                            defaults={
                                'vendor_name': safe_strip(row['Vendor Name']),
                                'gstin': safe_strip(row['GSTIN']),
                                'address': safe_strip(row['Address']),
                                'Pan_details': safe_strip(row['Pan Details']),
                                'Tally_ledger_creation': safe_strip(row['Tally Ledger Creation'])
                            }
                        )
                else:
                    raise ValueError("Worksheet named 'Vendor Code' not found")

                # Process sheet 3 - Part Number (tblPartNumber)
                if any(name.strip() == 'Part Number( Stock)' for name in sheet_names):
                    df_part_number = pd.read_excel(xls, sheet_name=[name for name in sheet_names if name.strip() == 'Part Number( Stock)'][0])

                    # Log column names for debugging
                    print("Columns in 'Part Number( Stock)' sheet:", df_part_number.columns.tolist())

                    for _, row in df_part_number.iterrows():
                        try:
                            # Safely handle 'UQC', 'HSN', and other potential missing columns
                            uqc_value = safe_strip(row.get('UQC', ''))  # Get 'UQC' or default to ''
                            hsn_value = safe_strip(row.get('HSN', ''))  # Get 'HSN' or default to ''

                            tblPartNumber.objects.update_or_create(
                                part_number=safe_strip(row['Part Numer']),  # Assuming part_number is unique
                                defaults={
                                    'part_name': safe_strip(row['Part Name']),
                                    'vendor_name': safe_strip(row['Vendor Name']),
                                    'project_name': safe_strip(row['Project Name']),
                                    'description': safe_strip(row['Description']),
                                    'hsn': hsn_value,  # Use safely fetched HSN
                                    'invoice_number': safe_strip(row['Invoice number']),
                                    'gst_rate': row['GST Rate(%)'],  # No need for strip on numerical values
                                    'date_of_invoice': pd.to_datetime(row['Date of invoice']).date(),
                                    'uqc': uqc_value,  # Use safely fetched UQC value
                                    'invoice_value': row['Invoice value'],
                                    'qty': row['Qty'],
                                    'cost_per_unit': row['Cost pu'],
                                    'total_invoice': row['Total Invoice'],
                                    'payment_status': safe_strip(row['Payment status']),
                                    'paid_date': pd.to_datetime(row['Paid Date']).date() if pd.notna(row['Paid Date']) else None,
                                    'paid_by': safe_strip(row.get('Paid By', '')),  # Handle optional 'Paid By'
                                    'type': safe_strip(row['Type']),
                                    'gstr2b': safe_strip(row.get('GSTR2B', '')),  # Handle optional 'GSTR2B'
                                    'remarks': safe_strip(row.get('Remarks', '')),  # Handle optional 'Remarks'
                                    'ledger': safe_strip(row.get('Ledger', ''))  # Handle optional 'Ledger'
                                }
                            )
                        except KeyError as e:
                            print(f"Missing column in Part Number sheet: {e}")
                            raise
                else:
                    raise ValueError("Worksheet named 'Part Number( Stock)' not found")

                messages.success(request, "Data updated successfully!")
                return redirect('bulk_update_view')

            except Exception as e:
                messages.error(request, f"Bulk Uploaded..Project,PartNumber,VendorDetails")
                return redirect('bulk_update_view')
    else:
        form = UploadFileForm()

    return render(request, 'bulk_update.html', {'form': form})



#------------------------------------------------- Project -----------------------------

from django.shortcuts import render, redirect, get_object_or_404
from .models import tblProject
from .forms import ProjectForm,vendordetailsForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
import pandas as pd
from io import BytesIO

def tblProject_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        project_id = request.POST.get('project_id')
        print('action =', action,'project_id =',project_id )

        if action == 'insert':
            form = ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('tblProject')

        elif action == 'update':
            project = get_object_or_404(tblProject, id=project_id)
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect('tblProject')

        elif action == 'delete':
            project = get_object_or_404(tblProject, id=project_id)
            project.delete()
            return redirect('tblProject')

        elif action == 'download_template':
            wb = Workbook()
            ws = wb.active
            ws.title = 'Project_Template'
            headers = ['Company Name', 'Company Code', 'Project Name', 'Project Code', 'Part Number', 'Part Name']
            ws.append(headers)

            buffer = BytesIO()
            wb.save(buffer)
            buffer.seek(0)

            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="Project_Template.xlsx"'
            return response

        elif action == 'bulk_insert':
            xlsx_file = request.FILES.get('xlsx_file')
            if not xlsx_file:
                return HttpResponse("No file uploaded.", status=400)

            try:
                df = pd.read_excel(xlsx_file, engine='openpyxl', dtype=str)
                column_mapping = {
                    'Company Name': 'company_name',
                    'Company Code': 'company_code',
                    'Project Name1': 'project_name1',
                    'ProjectCode1': 'project_code1',
                    'ProjCode- Partnumber': 'projcode_partnumber',
                    'ProjCode-Partname': 'projcode_partname',
                }

                if not set(column_mapping.keys()).issubset(df.columns.str.strip()):
                    missing_cols = set(column_mapping.keys()) - set(df.columns.str.strip())
                    return HttpResponse(f"Error: Missing columns in the file: {missing_cols}", status=400)

                df = df.rename(columns=column_mapping)

                for _, row in df.iterrows():
                    tblProject.objects.update_or_create(
                        company_code=row['company_code'],
                        defaults={
                            'company_name': row['company_name'],
                            'project_name': row['project_name1'],
                            'project_code': row['project_code1'],
                            'projcode_partnumber': row['projcode_partnumber'],
                            'projcode_partname': row['projcode_partname'],
                        }
                    )

                return redirect('tblProject')

            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=500)

        elif action == 'download_project_details':
            wb = Workbook()
            ws = wb.active
            ws.title = "Project Details"
            headers = ['Company Name', 'Company Code', 'Project Name', 'Project Code', 'Part Number', 'Part Name']
            ws.append(headers)

            data = tblProject.objects.all()
            for obj in data:
                ws.append([
                    obj.company_name, obj.company_code, obj.project_name, 
                    obj.project_code, obj.projcode_partnumber, obj.projcode_partname
                ])

            buffer = BytesIO()
            wb.save(buffer)
            buffer.seek(0)

            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="Project_Details.xlsx"'
            return response

    search_query = request.GET.get('search', '')
    project_data = tblProject.objects.all()

    if search_query:
        project_data = project_data.filter(project_name1__icontains=search_query) | project_data.filter(
            company_name__icontains=search_query
        ) | project_data.filter(
            projcode_partname__icontains=search_query
        )

    paginator = Paginator(project_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = ProjectForm()  # Initialize the form for new insertions

    return render(request, 'tblProjectForm.html', {'form': form, 'project_data': page_obj, 'search_query': search_query})


#-------------------------------------------------


import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import tblPartNumber
import datetime

def parse_date(value):
    """Helper function to parse and format date fields."""
    try:
        if pd.isna(value):
            return None
        # If it's already a date or datetime object, format it
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.strftime('%Y-%m-%d')
        # Try converting string dates in various formats
        return pd.to_datetime(value).strftime('%Y-%m-%d')
    except Exception:
        return None

def part_number_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'insert':
            part_number = request.POST.get('part_number')
            part_name = request.POST.get('part_name')
            vendor_name = request.POST.get('vendor_name')
            project_name = request.POST.get('project_name')
            description = request.POST.get('description')
            hsn = request.POST.get('hsn')
            invoice_number = request.POST.get('invoice_number')
            gst_rate = request.POST.get('gst_rate')
            date_of_invoice = request.POST.get('date_of_invoice')
            uqc = request.POST.get('uqc')
            invoice_value = request.POST.get('invoice_value')
            qty = request.POST.get('qty')
            cost_per_unit = request.POST.get('cost_per_unit')
            total_invoice = request.POST.get('total_invoice')
            payment_status = request.POST.get('payment_status')
            paid_date = request.POST.get('paid_date')
            paid_by = request.POST.get('paid_by')
            type_ = request.POST.get('type')
            gstr2b = request.POST.get('gstr2b')
            remarks = request.POST.get('remarks')
            ledger = request.POST.get('ledger')

            # Create the part number entry in the database
            tblPartNumber.objects.create(
                part_number=part_number,
                part_name=part_name,
                vendor_name=vendor_name,
                project_name=project_name,
                description=description,
                hsn=hsn,
                invoice_number=invoice_number,
                gst_rate=gst_rate,
                date_of_invoice=date_of_invoice,
                uqc=uqc,
                invoice_value=invoice_value,
                qty=qty,
                cost_per_unit=cost_per_unit,
                total_invoice=total_invoice,
                payment_status=payment_status,
                paid_date=paid_date,
                paid_by=paid_by,
                type=type_,
                gstr2b=gstr2b,
                remarks=remarks,
                ledger=ledger
            )
            
            return redirect('tblPartNumber')# Redirect after successful insertion

        # Handle bulk insert from Excel
        elif action == 'bulk_insert':
            excel_file = request.FILES.get('xlsx_file')
            if not excel_file:
                return HttpResponse("Error: No file uploaded", status=400)

            file_extension = excel_file.name.split('.')[-1]
            if file_extension != 'xlsx':
                return HttpResponse("Unsupported file format", status=400)

            try:
                df = pd.read_excel(excel_file, engine='openpyxl')
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')  # Normalize column names
                
                required_columns = {'part_numer', 'part_name', 'vendor_name', 'project_name', 'description', 'hsn',
                                    'invoice_number', 'gst_rate(%)', 'date_of_invoice', 'uqc', 'invoice_value', 'qty', 
                                    'cost_pu', 'total_invoice', 'payment_status', 'paid_date', 'paid_by', 'type', 
                                    'gstr2b', 'remarks', 'ledger'}
                
                if not required_columns.issubset(df.columns):
                    missing_cols = required_columns - set(df.columns)
                    return HttpResponse(f"Error: Missing columns in the file: {missing_cols}", status=400)

                # Iterate over each row and update or create the part number
                for _, row in df.iterrows():
                    # Use parse_date() to clean and format the date fields
                    date_of_invoice = parse_date(row.get('date_of_invoice'))
                    
                    paid_date = parse_date(row.get('paid_date'))
                    print(row.get('gstr2b'))
                    

                    tblPartNumber.objects.update_or_create(
                        part_number=row['part_numer'],
                        defaults={
                            'part_name': row['part_name'],
                            'vendor_name': row['vendor_name'],
                            'project_name': row['project_name'],
                            'description': row['description'],
                            'hsn': row['hsn'],
                            'invoice_number': row['invoice_number'],
                            'gst_rate': row['gst_rate(%)'],
                            'date_of_invoice': date_of_invoice,  # Cleaned and validated date
                            'uqc': row['uqc'],
                            'invoice_value': row['invoice_value'],
                            'qty': row['qty'],
                            'cost_per_unit': row['cost_pu'],
                            'total_invoice': row['total_invoice'],
                            'payment_status': row['payment_status'],
                            'paid_date': paid_date,  # Cleaned and validated date
                            'paid_by': row['paid_by'],
                            'type': row['type'],
                            'gstr2b': row['gstr2b'],
                            'remarks': row['remarks'],
                            'ledger': row['ledger']
                        }
                    )
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=500)

            return redirect('tblPartNumber')  # Redirect after successful bulk insert

    search_query = request.GET.get('search', '')
    project_data = tblPartNumber.objects.all()

    if search_query:
        project_data = project_data.filter(project_name1__icontains=search_query) | project_data.filter(
            company_name__icontains=search_query
        ) | project_data.filter(
            projcode_partname__icontains=search_query
        )

    paginator = Paginator(project_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tblpartnumber.html', {'data': page_obj, 'search_query': search_query})





#-----------------------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import tblVendordetails
from django.core.paginator import Paginator
import pandas as pd

def Vendordetails(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        
        # Handling single insert
        if action == 'insert':
            vendor_name = request.POST.get('vendor_name')
            vendor_code = request.POST.get('vendor_code')
            gstin = request.POST.get('gstin')
            address = request.POST.get('address')
            pan_details = request.POST.get('Pan_details')
            tally_ledger_creation = request.POST.get('Tally_ledger_creation')
            
            tblVendordetails.objects.create(
                vendor_name=vendor_name,
                vendor_code=vendor_code,
                gstin=gstin,
                address=address,
                Pan_details=pan_details,
                Tally_ledger_creation=tally_ledger_creation
            )
            return redirect('Vendordetails')
        
        # Handling bulk insert
        elif action == 'bulk_insert':
            ex_file = request.FILES.get('xlsx_file')
            if not ex_file:
                return HttpResponse("Error: No file uploaded", status=400)
            
            file_extension = ex_file.name.split('.')[-1]
            if file_extension != 'xlsx':
                return HttpResponse("Unsupported file format", status=400)
            
            try:
                df = pd.read_excel(ex_file, engine='openpyxl', skiprows=1)
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                required_columns = {'vendor_name', 'vendor_code', 'gstin', 'address', 'pan_details', 'tally_ledger_creation'}
                
                if not required_columns.issubset(df.columns):
                    missing_cols = required_columns - set(df.columns)
                    return HttpResponse(f"Error: Missing columns in the file: {missing_cols}", status=400)
                
                for _, row in df.iterrows():
                    tblVendordetails.objects.update_or_create(
                        vendor_code=row['vendor_code'],
                        defaults={
                            'vendor_name': row['vendor_name'],
                            'gstin': row['gstin'],
                            'address': row['address'],
                            'Pan_details': row['pan_details'],
                            'Tally_ledger_creation': row['tally_ledger_creation']
                        }
                    )
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=500)
            
            return redirect('Vendordetails')
    
    # Search and pagination
    search_query = request.GET.get('search', '')
    vendor_data = tblVendordetails.objects.all()
    
    if search_query:
        vendor_data = vendor_data.filter(
            vendor_name__icontains=search_query
        ) | vendor_data.filter(
            vendor_code__icontains=search_query
        ) | vendor_data.filter(
            gstin__icontains=search_query
        )
    
    paginator = Paginator(vendor_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendordetails.html', {'data': page_obj, 'search_query': search_query})





#----------------------------------------------------------------------


import pandas as pd
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.db import transaction, IntegrityError
from .models import CreateVendor, CreateCustomer, CreateProject, UploadInvoicefromVendor
from .forms import CreateVendorForm, CreateCustomerForm, CreateProjectForm, UploadInvoicefromVendorForm


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def CreateVendor_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        vendor_id = request.POST.get('vendor_id')
        print('action',action)
        print('vendor_id',vendor_id)

        if action == 'insert':
            form = CreateVendorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CreateVendor')

        elif action == 'update':
            vendor = get_object_or_404(CreateVendor, VENDID=vendor_id)
            form = CreateVendorForm(request.POST, instance=vendor)
            if form.is_valid():
                form.save()
                return redirect('CreateVendor')
        elif action == 'delete':
            vendor = get_object_or_404(CreateVendor, VENDID=vendor_id)
            vendor.delete()
            return redirect('CreateVendor')  

        elif action == 'bulk_insert':
            try:
                excel_file = request.FILES['xlsx_file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                filepath = fs.path(filename)

                # Read the Excel file into a DataFrame
                df = pd.read_excel(filepath)

                # Log the number of rows read
                logger.debug(f"Number of rows in Excel file: {len(df)}")

                # Prepare a list of CreateVendor instances to be updated or created
                vendors_to_update = []

                for _, row in df.iterrows():
                    vendor_id = str(row['Vendor ID']).strip()
                    vendor_name = str(row['Vendor Name']).strip()
                    vendor_gstin = str(row['Vendor GSTIN']).strip()
                    vendor_address = str(row['Vendor Address']).strip()
                    vendor_pan = str(row['Vendor PAN']).strip()
                    type_of_vendor = str(row['Type of Vendor']).strip()
                    bank_acc = str(row['Bank Acc']).strip()
                    ifsc_code = str(row['IFSC']).strip()
                    branch_name = str(row['Branch']).strip()

                    vendor = CreateVendor(
                        VENDID=vendor_id,
                        VendorNAme=vendor_name,
                        VEndorGSTIN=vendor_gstin,
                        VendorAddress=vendor_address,
                        VendorPAN=vendor_pan,
                        TypeofVendor=type_of_vendor,
                        BankAcc=bank_acc,
                        IFSC=ifsc_code,
                        Branch=branch_name
                    )
                    vendors_to_update.append(vendor)

                # Use transaction.atomic to ensure all-or-nothing operation
                with transaction.atomic():
                    for vendor in vendors_to_update:
                        try:
                            CreateVendor.objects.update_or_create(
                                VENDID=vendor.VENDID,
                                defaults={
                                    'VendorNAme': vendor.VendorNAme,
                                    'VEndorGSTIN': vendor.VEndorGSTIN,
                                    'VendorAddress': vendor.VendorAddress,
                                    'VendorPAN': vendor.VendorPAN,
                                    'TypeofVendor': vendor.TypeofVendor,
                                    'BankAcc': vendor.BankAcc,
                                    'IFSC': vendor.IFSC,
                                    'Branch': vendor.Branch,
                                }
                            )
                        except IntegrityError as e:
                            logger.error(f"Error updating or creating vendor {vendor.VENDID}: {e}")

                return redirect('CreateVendor')

            except Exception as e:
                logger.error(f"Error processing file: {e}")
                return render(request, 'vendordetails.html', {
                    'form': CreateVendorForm(),
                    'vendors': CreateVendor.objects.all(),
                    'error': f"Error processing file: {e}"
                })

    else:
        form = CreateVendorForm()
        vendors = CreateVendor.objects.all()

    return render(request, 'vendordetails.html', {
        'form': form,
        'vendors': vendors
    })

    
    
#--------------------------------------------------------------------------------------
import pandas as pd
from django.db import transaction

def CreateCustomer_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        customer_id = request.POST.get('customer_id')
        print(action,customer_id)

        if action == 'insert':
            form = CreateCustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CreateCustomer')

        elif action == 'update':
            customer = get_object_or_404(CreateCustomer, CUSTID=customer_id)
            form = CreateCustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('CreateCustomer')

        elif action == 'delete':
            customer = get_object_or_404(CreateCustomer, CUSTID=customer_id)
            customer.delete()
            return redirect('CreateCustomer')

        elif action == 'bulk_insert':
            try:
                excel_file = request.FILES['xlsx_file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                filepath = fs.path(filename)

                # Read Excel file into DataFrame
                df = pd.read_excel(filepath)

                # Check if required columns exist
                required_columns = [
                    'Customer ID', 'Customer Name', 'Customer GSTIN',
                    'Customer Address', 'Customer PAN', 'Type of Customer',
                    'Bank Acc', 'IFSC', 'Branch'
                ]
                if not all(col in df.columns for col in required_columns):
                    raise ValueError("Missing required columns in Excel file")

                # Start a transaction to bulk insert/update
                with transaction.atomic():
                    for _, row in df.iterrows():
                        try:
                            cust_id = str(row['Customer ID']).strip()
                            customer_name = str(row['Customer Name']).strip()
                            customer_gstin = str(row['Customer GSTIN']).strip()
                            customer_address = str(row['Customer Address']).strip()
                            customer_pan = str(row['Customer PAN']).strip()
                            type_of_customer = str(row['Type of Customer']).strip()
                            bank_acc = str(row['Bank Acc']).strip()
                            ifsc_code = str(row['IFSC']).strip()
                            branch_name = str(row['Branch']).strip()

                            if not cust_id or not customer_name or not customer_gstin:
                                raise ValueError(f"Missing data in row: {row}")

                            # Use update_or_create to ensure records are inserted/updated properly
                            CreateCustomer.objects.update_or_create(
                                CUSTID=cust_id,
                                defaults={
                                    'CustomerName': customer_name,
                                    'CustomerGSTIN': customer_gstin,
                                    'CustomerADdress': customer_address,
                                    'CustomerPAN': customer_pan,
                                    'TypeofCustomer': type_of_customer,
                                    'BankAcc': bank_acc,
                                    'IFSC': ifsc_code,
                                    'Branch': branch_name,
                                }
                            )
                        except Exception as e:
                            print(f"Error processing row {row}: {e}")

                return redirect('CreateCustomer')

            except Exception as e:
                return render(request, 'CreateCustomer.html', {
                    'form': CreateCustomerForm(),
                    'custr': CreateCustomer.objects.all(),
                    'error': f"Error processing file: {e}"
                })

    else:
        form = CreateCustomerForm()

    custr = CreateCustomer.objects.all()

    return render(request, 'CreateCustomer.html', {
        'form': form,
        'custr': custr
    })


#========================================================================================================================================================


from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import pandas as pd
from .models import InternationalCustomers
from .forms import InternationalCustomersForm

def international_customer_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        customer_id = request.POST.get('customer_id')
        print(action, customer_id)

        if action == 'insert':
            form = InternationalCustomersForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('international_customer')

        elif action == 'update':
            customer = get_object_or_404(InternationalCustomers, cust_id=customer_id)
            form = InternationalCustomersForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('international_customer')

        elif action == 'delete':
            customer = get_object_or_404(InternationalCustomers, cust_id=customer_id)
            customer.delete()
            return redirect('international_customer')

        elif action == 'bulk_insert':
            try:
                excel_file = request.FILES['xlsx_file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                filepath = fs.path(filename)

                # Read Excel file into DataFrame
                df = pd.read_excel(filepath)

                # Check if required columns exist
                required_columns = [
                    'Customer Name', 'Customer ID', 'Address', 'Type of Customer', 'Swift Code',
                    'Branch', 'ABA Routing Code'
                ]

                if not all(col in df.columns for col in required_columns):
                    raise ValueError("Missing required columns in Excel file")

                # Start a transaction to bulk insert/update
                with transaction.atomic():
                    for _, row in df.iterrows():
                        try:
                            customername = str(row['Customer Name']).strip()
                            custid = str(row['Customer ID']).strip()
                            custaddress = str(row['Address']).strip()
                            typeofcustomer = str(row['Type of Customer']).strip()
                            accountnumber = str(row.get('Account Number', '')).strip()  # Added get for optional column
                            swiftcode = str(row['Swift Code']).strip()
                            branchdetails = str(row['Branch']).strip()
                            abaroutingcode = str(row['ABA Routing Code']).strip()

                            if not custid or not customername or not typeofcustomer:
                                raise ValueError(f"Missing data in row: {row}")

                            # Use update_or_create to ensure records are inserted/updated properly
                            InternationalCustomers.objects.update_or_create(
                                cust_id=custid,
                                defaults={
                                    'customer_name': customername,
                                    'address': custaddress,
                                    'type_of_customer': typeofcustomer,
                                    'account_number': accountnumber,
                                    'swift_code': swiftcode,
                                    'branch': branchdetails,
                                    'aba_routing_code': abaroutingcode,
                                }
                            )
                        except Exception as e:
                            print(f"Error processing row {row}: {e}")

                return redirect('international_customer')

            except Exception as e:
                return render(request, 'international_customer.html', {
                    'form': InternationalCustomersForm(),
                    'custr': InternationalCustomers.objects.all(),
                    'error': f"Error processing file: {e}"
                })

    else:
        form = InternationalCustomersForm()

    custr = InternationalCustomers.objects.all()

    return render(request, 'international_customer.html', {
        'form': form,
        'custr': custr
    })

from .models import InternationalCustomers2
from .forms import InternationalCustomersForm2
def international_customer_2(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        customer_id = request.POST.get('customer_id')
        print(action, customer_id)

        if action == 'insert':
            form = InternationalCustomersForm2(request.POST)
            if form.is_valid():
                form.save()
                return redirect('international_customer_2')

        elif action == 'update':
            customer = get_object_or_404(InternationalCustomers2, cust_id=customer_id)
            form = InternationalCustomersForm2(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('international_customer_2')

        elif action == 'delete':
            customer = get_object_or_404(InternationalCustomers2, cust_id=customer_id)
            customer.delete()
            return redirect('international_customer_2')

        elif action == 'bulk_insert':
            try:
                excel_file = request.FILES['xlsx_file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                filepath = fs.path(filename)

                # Read Excel file into DataFrame
                df = pd.read_excel(filepath)

                # Check if required columns exist
                required_columns = [
                    'Customer Name', 'Customer ID', 'Address', 'Type of Customer', 'Swift Code',
                    'Branch', 'ABA Routing Code'
                ]

                if not all(col in df.columns for col in required_columns):
                    raise ValueError("Missing required columns in Excel file")

                # Start a transaction to bulk insert/update
                with transaction.atomic():
                    for _, row in df.iterrows():
                        try:
                            customername = str(row['Customer Name']).strip()
                            custid = str(row['Customer ID']).strip()
                            custaddress = str(row['Address']).strip()
                            typeofcustomer = str(row['Type of Customer']).strip()
                            accountnumber = str(row.get('Account Number', '')).strip()  # Added get for optional column
                            swiftcode = str(row['Swift Code']).strip()
                            branchdetails = str(row['Branch']).strip()
                            abaroutingcode = str(row['ABA Routing Code']).strip()

                            if not custid or not customername or not typeofcustomer:
                                raise ValueError(f"Missing data in row: {row}")

                            # Use update_or_create to ensure records are inserted/updated properly
                            InternationalCustomers2.objects.update_or_create(
                                cust_id=custid,
                                defaults={
                                    'customer_name': customername,
                                    'address': custaddress,
                                    'type_of_customer': typeofcustomer,
                                    'account_number': accountnumber,
                                    'swift_code': swiftcode,
                                    'branch': branchdetails,
                                    'aba_routing_code': abaroutingcode,
                                }
                            )
                        except Exception as e:
                            print(f"Error processing row {row}: {e}")

                return redirect('international_customer_2')

            except Exception as e:
                return render(request, 'in_customer.html', {
                    'form': InternationalCustomersForm2(),
                    'custr': InternationalCustomers2.objects.all(),
                    'error': f"Error processing file: {e}"
                })

    else:
        form = InternationalCustomersForm2()

    custr = InternationalCustomers2.objects.all()

    return render(request, 'in_customer.html', {
        'form': form,
        'custr': custr
    })






#---------------------------------working CreateProject_view---------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProjectForm
from .models import CreateProject
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

def CreateProject_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        project_id = request.POST.get('project_id')
        print("Action:", action)  # Debug statement
        print("POST Data:", request.POST)  # Debug statement

        # Insert a new project
        if action == 'insert':
            form = CreateProjectForm(request.POST)
            if form.is_valid():
                print("Form is valid.") 
                form.save()
                messages.success(request, "Project inserted successfully.")
                return redirect('CreateProject')
            else:
                messages.error(request, "Error inserting project. Please check the form inputs.")
        
        # Update an existing project
        elif action == 'update':
            project = get_object_or_404(CreateProject, PROJID=project_id)
            form = CreateProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                messages.success(request, "Project updated successfully.")
                return redirect('CreateProject')
            else:
                messages.error(request, "Error updating project. Please check the form inputs.")
        
        # Delete an existing project
        elif action == 'delete':
            project = get_object_or_404(CreateProject, PROJID=project_id)
            project.delete()
            messages.success(request, "Project deleted successfully.")
            return redirect('CreateProject')
        
        # Bulk insert projects from Excel file
        elif action == 'bulk_insert':
            excel_file = request.FILES.get('xlsx_file')
            if excel_file:
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                file_path = fs.path(filename)

                try:
                    # Read the Excel file
                    df = pd.read_excel(file_path)
                    for _, row in df.iterrows():
                        CreateProject.objects.update_or_create(
                            PROJID=row['PROJID'],
                            defaults={
                                'CUSTID': row['CUSTID'],
                                'CustomerName': row['CustomerName'],
                                'ProjectNAme': row['ProjectNAme'],
                                'Description': row['Description'],
                                'ProjCodePArtNumberSuffix': row['ProjCodePArtNumberSuffix'],
                                'ProjCodePartNameSuffix': row['ProjCodePartNameSuffix'],
                                'FY': row['FY'],
                            }
                        )
                    messages.success(request, "Projects uploaded successfully from the Excel file.")
                except Exception as e:
                    messages.error(request, f"Error processing Excel file: {str(e)}")
            else:
                messages.error(request, "No file uploaded. Please select a valid Excel file.")
            return redirect('CreateProject')

    # For GET requests, render the form and table
    form = CreateProjectForm()
    projects = CreateProject.objects.all()
    return render(request, 'CreateProject.html', {'form': form, 'projects': projects})

#-------------------------------------------------------------------------



# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UploadInvoicefromVendor,CreateInvoiceBasedPartNumber,CreatePurchaseBasedCosting
from .forms import UploadInvoicefromVendorForm,CreateInvoiceBasedPartNumberForm,CreatePurchaseBasedCostingForm




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UploadInvoicefromVendor
from .forms import UploadInvoicefromVendorForm


#----------------------18-11-24 below updating code -------------------
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadInvoicefromVendorForm
from .models import UploadInvoicefromVendor, CreateProject
import logging
from datetime import datetime


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def UploadInvoicefromVendor_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        Vendor_id = request.POST.get('vendor_id')
        print(action, Vendor_id)

        if action == 'insert':
            form = UploadInvoicefromVendorForm(request.POST, request.FILES)
            if form.is_valid():
                invoice = form.save(commit=False)
                try:
                    project = CreateProject.objects.get(PROJID=invoice.PROJID)
                    invoice.Part_number = f"{project.FY}-{project.ProjCodePArtNumberSuffix}-{invoice.VENDID}-{invoice.VendorInvoiceNumber}"
                    invoice.Part_name = f"{project.FY}-{project.ProjCodePartNameSuffix}-{invoice.VENDID}-{invoice.VendorInvoiceNumber}"
                except CreateProject.DoesNotExist:
                    invoice.Part_number = "Invalid Project ID"
                    invoice.Part_name = "Invalid Project Name"

                try:
                    invoice_value = float(invoice.InvoiceValue)
                    qty_received = float(invoice.QtyReceived)
                    invoice.CostPerunit = "{:.2f}".format(invoice_value / qty_received)
                except (ValueError, ZeroDivisionError):
                    invoice.CostPerunit = "Error in calculation"

                try:
                    invoice_value = float(invoice.InvoiceValue)
                    gst_rate = float(invoice.GSTRate.strip('%')) / 100
                    invoice.TotalValue = "{:.2f}".format(invoice_value * (1 + gst_rate))
                except ValueError:
                    invoice.TotalValue = "Error in calculation"

                try:
                    invoice_value = float(invoice.InvoiceValue)
                    gst_rate = float(invoice.GSTRate.strip('%')) / 100
                    if invoice.OptionType == 'LOCAL':
                        invoice.CGST = "{:.2f}".format(invoice_value * gst_rate / 2)
                        invoice.SGST = "{:.2f}".format(invoice_value * gst_rate / 2)
                        invoice.IGST = "0"
                    elif invoice.OptionType == 'INTERSTATE':
                        invoice.CGST = "0"
                        invoice.SGST = "0"
                        invoice.IGST = "{:.2f}".format(invoice_value * gst_rate)
                except ValueError:
                    invoice.CGST = invoice.SGST = invoice.IGST = "Error in calculation"

                invoice.save()
                messages.success(request, 'Invoice inserted successfully.')
            else:
                messages.error(request, 'Form submission failed. Please correct the errors.')

        elif action == 'update':
            data_instance = get_object_or_404(UploadInvoicefromVendor, VENDID=Vendor_id)
            form = UploadInvoicefromVendorForm(request.POST, instance=data_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Invoice updated successfully.')
            else:
                messages.error(request, 'Error updating invoice. Please correct the form errors.')

        elif action == 'delete':
            data_instance = get_object_or_404(UploadInvoicefromVendor, VENDID=Vendor_id)
            data_instance.delete()
            messages.success(request, 'Invoice deleted successfully.')
            return redirect('UploadInvoicefromVendor')

        elif action == 'bulk_insert':
            file = request.FILES.get('xlsx_file')
            if file:
                try:
                    # Read Excel data
                    data = pd.read_excel(file)
                    required_columns = [
                        "PROJID", "VENDID", "VendorInvoiceNumber", "VendorNAme",
                        "DateofInvoice", "UnitOfMeasure", "QtyReceived", "GSTRate",
                        "InvoiceValue", "HSN", "CostPerunit", "TotalValue",
                        "Part_number", "Part_name", "CGST", "SGST", "IGST", "OptionType"
                    ]
                    missing_columns = [col for col in required_columns if col not in data.columns]
                    

                    if missing_columns:
                        messages.error(request, f"Missing columns: {', '.join(missing_columns)}")
                    else:
                        for _, row in data.iterrows():
                            try:
                                row_data = row.where(pd.notnull(row), None)
        
     
                                if row_data["DateofInvoice"]:
                                # Ensure DateofInvoice is a string
                                    if isinstance(row_data["DateofInvoice"], pd.Timestamp):
                                        date_obj = row_data["DateofInvoice"].to_pydatetime()
                                    else:
                                        date_obj = datetime.strptime(row_data["DateofInvoice"], '%Y-%m-%d %H:%M:%S')  # Adjust format if needed
                                
                                    row_data["DateofInvoice"] = date_obj.strftime('%d-%m-%Y')

                                UploadInvoicefromVendor.objects.update_or_create(
                                    VendorInvoiceNumber=row_data["VendorInvoiceNumber"],
                                    defaults={
                                        "PROJID": row_data["PROJID"],
                                        "VENDID": int(row_data["VENDID"]),
                                        "VendorNAme": row_data["VendorNAme"],
                                        "DateofInvoice": row_data["DateofInvoice"],
                                        "UnitOfMeasure": row_data["UnitOfMeasure"],
                                        "QtyReceived": int(row_data["QtyReceived"]),
                                        "GSTRate": f'{int(float(row_data["GSTRate"])*100)}%',
                                        "InvoiceValue": "{:.2f}".format(row_data["InvoiceValue"]),
                                        "HSN": row_data["HSN"],
                                        "CostPerunit":"{:.2f}".format( row_data["CostPerunit"]),
                                        "TotalValue": row_data["TotalValue"],
                                        "Part_number": row_data["Part_number"],
                                        "Part_name": row_data["Part_name"],
                                        "CGST": "{:.2f}".format((row_data["CGST"])),
                                        "SGST": "{:.2f}".format(row_data["SGST"]),
                                        "IGST": "{:.2f}".format(row_data["IGST"]),
                                        "OptionType": row_data["OptionType"],
                                    },
                                )
                            except Exception as e:
                                logger.error(f"Error processing row with VendorInvoiceNumber {row['VendorInvoiceNumber']}: {e}")
                        messages.success(request, 'Bulk insertion completed successfully.')

                except Exception as e:
                    messages.error(request, f"Error processing file: {e}")
                    logger.error(f"Error processing file: {e}")
            else:
                messages.error(request, 'No file uploaded. Please upload an Excel file.')

    form = UploadInvoicefromVendorForm()
    invoices = UploadInvoicefromVendor.objects.all()
    
    context = {
        'form': form,
        'invoices': invoices,
    }
    return render(request, 'UploadInvoicefromVendor.html', context)


   


        
#-------------------------------------------------------------------------
 
  
def CreateInvoiceBasedPartNumber_view(request):
    form = CreateInvoiceBasedPartNumberForm()
    data = CreateInvoiceBasedPartNumber.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        Vendor_id = request.POST.get('vendor_id')  
        
        try:
            if action == 'insert':
                form = CreateInvoiceBasedPartNumberForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Part Name. Part Number Created successfully.')
                else:
                    messages.error(request, 'Error adding invoice. Please correct the form errors.')

            elif action == 'update':
                data_instance = get_object_or_404(CreateInvoiceBasedPartNumber, VENDID=Vendor_id)
                form = CreateInvoiceBasedPartNumberForm(request.POST, instance=data_instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Invoice updated successfully.')
                else:
                    messages.error(request, 'Error updating invoice. Please correct the form errors.')

            elif action == 'delete':
                data_instance = get_object_or_404(CreateInvoiceBasedPartNumber, VENDID=Vendor_id)
                data_instance.delete()
                messages.success(request, 'Invoice deleted successfully.')

            else:
                messages.error(request, 'Invalid action.')

            return redirect('CreateInvoiceBasedPartNumber')

        except CreateInvoiceBasedPartNumber.DoesNotExist:
            messages.error(request, 'Invoice not found for the specified Vendor ID.')
            return redirect('CreateInvoiceBasedPartNumber')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('CreateInvoiceBasedPartNumber')

    context = {
        'form': form,
        'data': data
    }
    return render(request, 'CreateInvoiceBasedPartNumber.html', context)   

#-------------------------------------------------------------------------

#******************************************************************************************************************************************************



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .forms import CreatePurchaseBasedCostingForm
from .models import CreatePurchaseBasedCosting, UploadInvoicefromVendor

def CreatePurchaseBasedCosting_view(request):
    # Fetch distinct PROJID values for the choices
    projid_choices = [(proj_id, proj_id) for proj_id in UploadInvoicefromVendor.objects.values_list('PROJID', flat=True).distinct()]

    # Initialize the form with PROJID choices
    form = CreatePurchaseBasedCostingForm()
    form.fields['PROJID'].choices = projid_choices

    data = CreatePurchaseBasedCosting.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        cost_id = request.POST.get('COSTID')
        proj_id = request.POST.get('PROJID')

        try:
            if action == 'insert':
                form = CreatePurchaseBasedCostingForm(request.POST)
                form.fields['PROJID'].choices = projid_choices  # Ensure choices are set on form validation

                if form.is_valid():
                    # Fetch and calculate the sum of QtyReceived and TotalValue from UploadInvoicefromVendor
                    qty_sum = UploadInvoicefromVendor.objects.filter(PROJID=proj_id).aggregate(Sum('QtyReceived'))['QtyReceived__sum'] or 0
                    total_value_sum = UploadInvoicefromVendor.objects.filter(PROJID=proj_id).aggregate(Sum('TotalValue'))['TotalValue__sum'] or 0
                    
                    all_InvoiceValue = ', '.join(
                        UploadInvoicefromVendor.objects.filter(PROJID=proj_id).values_list('InvoiceValue', flat=True)
                    )
                    all_part_num = ', '.join(
                        UploadInvoicefromVendor.objects.filter(PROJID=proj_id).values_list('Part_number', flat=True)
                    )
                    all_Part_name = ', '.join(
                        UploadInvoicefromVendor.objects.filter(PROJID=proj_id).values_list('Part_name', flat=True)
                    )

                    # Save the record in CreatePurchaseBasedCosting
                    instance = form.save(commit=False)
                    instance.Qty = qty_sum
                    instance.TotalValue = total_value_sum
                    instance.InvoiceValues = all_InvoiceValue
                    instance.PartNums = all_part_num
                    instance.PartNames = all_Part_name                
                    instance.save()

                    messages.success(request, 'Record added successfully.')
                else:
                    messages.error(request, 'Error adding record. Please check the form fields.')

            elif action == 'update':
                data_instance = get_object_or_404(CreatePurchaseBasedCosting, COSTID=cost_id)
                form = CreatePurchaseBasedCostingForm(request.POST, instance=data_instance)
                form.fields['PROJID'].choices = projid_choices  # Ensure choices are set on form validation

                if form.is_valid():
                    # Update Qty and TotalValue based on the selected PROJID
                    qty_sum = UploadInvoicefromVendor.objects.filter(PROJID=proj_id).aggregate(Sum('QtyReceived'))['QtyReceived__sum'] or 0
                    total_value_sum = UploadInvoicefromVendor.objects.filter(PROJID=proj_id).aggregate(Sum('TotalValue'))['TotalValue__sum'] or 0

                    data_instance.Qty = qty_sum
                    data_instance.TotalValue = total_value_sum
                    data_instance.save()

                    messages.success(request, f'Record with COSTID {cost_id} updated successfully.')
                else:
                    messages.error(request, 'Error updating record. Please check the form fields.')

            elif action == 'delete':
                data_instance = get_object_or_404(CreatePurchaseBasedCosting, COSTID=cost_id)
                data_instance.delete()
                messages.success(request, f'Record with COSTID {cost_id} deleted successfully.')

            else:
                messages.error(request, 'Invalid action selected. Please choose a valid operation.')

            return redirect('CreatePurchaseBasedCosting')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('CreatePurchaseBasedCosting')

    context = {
        'form': form,
        'data': data
    }
    return render(request, 'CreatePurchaseBasedCosting.html', context)

#**********************************************************costing********************************************************************************************

from django.shortcuts import render
from .models import CreateProject

from django.shortcuts import render
from .models import CreateProject, UploadInvoicefromVendor, Costing

from django.shortcuts import render
from .models import Costing, CreateProject, UploadInvoicefromVendor


from django.shortcuts import render
from .models import Costing, CreateProject, UploadInvoicefromVendor

def project_dropdown_view(request):
    # Fetch all PROJID values from the CreateProject model
    projects = UploadInvoicefromVendor.objects.values_list('PROJID', flat=True).distinct()
    costing_entries = []

    if request.method == 'POST':
        proj_id_dd = request.POST.get('project_id')
        createproject_obj = CreateProject.objects.get(PROJID=proj_id_dd)
        cust_id = createproject_obj.CUSTID
        cust_name = createproject_obj.CustomerName
        project_name = createproject_obj.ProjectNAme

        # Fetch related UploadInvoicefromVendor objects
        upload_invoice_objs = UploadInvoicefromVendor.objects.filter(PROJID=proj_id_dd)

        # Process data into separate rows
        for invoice in upload_invoice_objs:
          costing_entries.append({
           "PROJID": proj_id_dd,
           "Project_name": project_name,
           "Custmer_id": cust_id,
           "Custmer_name": cust_name,
           "PartName": invoice.Part_name,
           "HSN": invoice.HSN,
           "GSTRate": invoice.GSTRate,
         "Qty": invoice.QtyReceived,
          "CostPerunit": invoice.CostPerunit,
          "TotalValue": invoice.TotalValue,
        })

        # Optionally update or create the Costing entry in the database
        Costing.objects.update_or_create(
            PROJID=proj_id_dd,
            defaults={
                'Project_name': project_name,
                'Custmer_id': cust_id,
                'Custmer_name': cust_name,
                'InvoiceValues': ', '.join([str(inv.InvoiceValue) for inv in upload_invoice_objs]),
                'PartNums': ', '.join([inv.Part_number for inv in upload_invoice_objs]),
                'PartNames': ', '.join([inv.Part_name for inv in upload_invoice_objs]),
                'Qty': ', '.join([str(inv.QtyReceived) for inv in upload_invoice_objs]),
                'TotalValue': ', '.join([str(inv.TotalValue) for inv in upload_invoice_objs]),
                'HSN': ', '.join([inv.HSN for inv in upload_invoice_objs]),
                'GSTRate': ', '.join([inv.GSTRate for inv in upload_invoice_objs]),
                'CostPerunit': ', '.join([inv.CostPerunit for inv in upload_invoice_objs]),
            }
        )



   # qty_sum = Costing.objects.filter(PROJID=proj_id_dd).aggregate(Sum('QtyReceived'))['QtyReceived__sum'] or 0

        # total_value_sum = Costing.objects.filter(PROJID=proj_id_dd).aggregate(Sum('TotalValue'))['TotalValue__sum'] or 0

                    

        # Fetch the newly created costing entries to display in the table

        # costing_entries = Costing.objects.filter(PROJID=proj_id_dd)



    # Pass processed entries to the template
    return render(request, 'costing.html', {'projects': projects, 'costing_entries': costing_entries})




# def project_dropdown_view(request):
#     # Fetch all PROJID values from the CreateProject model
#     projects = CreateProject.objects.values_list('PROJID', flat=True)
#     costing_entries = []

#     if request.method == 'POST':
#         proj_id_dd = request.POST.get('project_id')
#         createproject_obj = CreateProject.objects.get(PROJID=proj_id_dd)
#         cust_id = createproject_obj.CUSTID
#         cust_name = createproject_obj.CustomerName
#         project_name = createproject_obj.ProjectNAme

#         # Fetch related UploadInvoicefromVendor objects
#         upload_invoice_objs = UploadInvoicefromVendor.objects.filter(PROJID=proj_id_dd)

#         # Initialize empty lists to aggregate fields
#         invoice_values = []
#         part_nums = []
#         part_names = []
#         qty_received = []
#         total_values = []
#         hsn_codes = []
#         GSTRate =[]
#         CostPerunit = []

#         # Aggregate the fields into comma-separated strings
#         for invoice in upload_invoice_objs:
#             invoice_values.append(str(invoice.InvoiceValue))
#             part_nums.append(invoice.Part_number)
#             part_names.append(invoice.Part_name)
#             qty_received.append(str(invoice.QtyReceived))
#             total_values.append(str(invoice.TotalValue))
#             hsn_codes.append(invoice.HSN)
#             GSTRate.append(invoice.GSTRate)
#             CostPerunit.append(invoice.CostPerunit)

#         # Create a single string for each field
#         invoice_values_str = ', '.join(invoice_values)
#         part_nums_str = ', '.join(part_nums)
#         part_names_str = ', '.join(part_names)
#         qty_received_str = ', '.join(qty_received)
#         total_values_str = ', '.join(total_values)
#         hsn_codes_str = ', '.join(hsn_codes)
#         GSTRate_str  = ', '.join(GSTRate)
#         CostPerunit_str = ', '.join(CostPerunit)

#         # Update or create the Costing entry
#         Costing.objects.update_or_create(
#             PROJID=proj_id_dd,
#             defaults={
#                 'Project_name': project_name,
#                 'Custmer_id': cust_id,
#                 'Custmer_name': cust_name,
#                 'InvoiceValues': invoice_values_str,
#                 'PartNums': part_nums_str,
#                 'PartNames': part_names_str,
#                 'Qty': qty_received_str,
#                 'TotalValue': total_values_str,
#                 'HSN': hsn_codes_str,
#                 'GSTRate' : GSTRate_str,
#                 'CostPerunit' :CostPerunit_str,
                
#             }
#         )
#         # qty_sum = Costing.objects.filter(PROJID=proj_id_dd).aggregate(Sum('QtyReceived'))['QtyReceived__sum'] or 0
#         # total_value_sum = Costing.objects.filter(PROJID=proj_id_dd).aggregate(Sum('TotalValue'))['TotalValue__sum'] or 0
                    
#         # Fetch the newly created costing entries to display in the table
#         costing_entries = Costing.objects.filter(PROJID=proj_id_dd)

#     return render(request, 'costing.html', {'projects': projects, 'costing_entries': costing_entries})

#******************************************************************************************************************************************************



#-------------------------------------------------------------------------

from django.shortcuts import render
from django.contrib import messages
from .models import CreatePurchaseBasedCosting

def ReadPurchaseBasedCosting_view(request):
    # Fetch all unique project IDs for the dropdown
    all_projects = CreatePurchaseBasedCosting.objects.values_list('PROJID', flat=True).distinct()

    proj_id = request.GET.get('proj_id')
    data = None

    if proj_id:
        try:
            # Get data for the selected project ID
            data = CreatePurchaseBasedCosting.objects.get(PROJID=proj_id)
        except CreatePurchaseBasedCosting.DoesNotExist:
            # If no matching project is found
            messages.error(request, f"No data found for Project ID: {proj_id}")

    context = {
        'all_projects': all_projects,  # Pass all project IDs for the dropdown
        'data': data,  # Pass the selected project's data
    }
    return render(request, 'ReadPurchaseBasedCosting.html', context)




#-------------------------------------------qutation------------------------------
from django.http import JsonResponse
from django.shortcuts import render
from .models import CreateCustomer
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def qutation(request):
    if request.method == 'POST':
        c_id = request.POST.get('customer_id')
        try:
            cust_add = CreateCustomer.objects.get(CUSTID=c_id)
            c_add = cust_add.CustomerADdress
            print('Customer Address:', c_add)
            # Prepare the JSON response
            return JsonResponse({'customer_id': c_id, 'customer_address': c_add}, status=200)
        except CreateCustomer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
    
    # For GET requests or others, render the template
    c_id = CreateCustomer.objects.values_list('CUSTID', flat=True)
    return render(request, 'qutation.html', {'projects': c_id, 'cus_add': ''})











# def qutation(request):
    
#     c_id = CreateCustomer.objects.values_list('CUSTID', flat=True)
#     c_add = ''
#     if request.method =='POST':
#         c_id = request.POST.get('customer_id')
        

        
#         cust_add= CreateCustomer.objects.get(CUSTID = c_id)
#         c_add = cust_add.CustomerADdress
#         print('c_addvvvvvvvvvvvvvvvvvvvvvvvvvv:',c_add)
#         return render(request, 'qutation.html',{'projects': c_id,'cus_add': c_add })
#     return render(request, 'qutation.html',{'projects': c_id,'cus_add': c_add })
#=======================================================================================================================================================================================================================================from 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SchArtifactUploadForm
from .models import SchArtifactUpload

def SchArtifactUpload_view(request):
    form = SchArtifactUploadForm()
    projects = SchArtifactUpload.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        project_id = request.POST.get('PROJID')
        
        if action == 'insert':
            form = SchArtifactUploadForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Data inserted successfully.")
                return redirect('SchArtifactUpload')
            else:
                messages.error(request, "Error in data insert.")
        
        elif action == 'update':
            updata = get_object_or_404(SchArtifactUpload, PROJID=project_id)
            formdata = SchArtifactUploadForm(request.POST, instance=updata)
            if formdata.is_valid():
                formdata.save()
                messages.success(request, "Data updated successfully.")
                return redirect('SchArtifactUpload')
            else:
                messages.error(request, "Error in data update.")
        
        elif action == 'delete':
            data = get_object_or_404(SchArtifactUpload, PROJID=project_id)
            data.delete()
            messages.success(request, "Data deleted successfully.")
            return redirect('SchArtifactUpload')
    
    return render(request, 'SchArtifactUpload.html', {'form': form, 'projects': projects})

        
#=====================================================   Engg_bom_upload_view ==================================================================================================================================================================================

from django.shortcuts import render, redirect, get_object_or_404
from .models import EnggBOMUpload
from .forms import EnggBOMUploadForm

def engg_bom_upload_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'insert':
            form = EnggBOMUploadForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('engg_bom_upload')

        elif action == 'update':
            bom_id = request.POST.get('bom_id')
            instance = get_object_or_404(EnggBOMUpload, id=bom_id)
            form = EnggBOMUploadForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('engg_bom_upload')

        elif action == 'delete':
            bom_id = request.POST.get('bom_id')
            instance = get_object_or_404(EnggBOMUpload, id=bom_id)
            instance.delete()
            return redirect('engg_bom_upload')

    else:
        form = EnggBOMUploadForm()
    
    boms = EnggBOMUpload.objects.all()
    return render(request, 'EnggBOMUpload.html', {'form': form, 'boms': boms})


#=======================================================pcbartifactupload===============================================================================================================================================================================================================================
from django.shortcuts import render, redirect, get_object_or_404
from .models import PCBArtifactUpload
from .forms import PCBArtifactUploadForm

def pcbartifactupload_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pcb_id = request.POST.get('pcb_id')
        
        # Insert action
        if action == 'insert':
            form = PCBArtifactUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('pcbartifactupload_view')
        
        # Update action
        elif action == 'update':
            
            instance = get_object_or_404(PCBArtifactUpload, id=pcb_id)
            form = PCBArtifactUploadForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('pcbartifactupload_view')
        
        # Delete action
        elif action == 'delete':
            pcb_id = request.POST.get('pcb_id')
            instance = get_object_or_404(PCBArtifactUpload, id=pcb_id)
            instance.delete()
            return redirect('pcbartifactupload_view')
    
    form = PCBArtifactUploadForm()
    pcbs = PCBArtifactUpload.objects.all()
    return render(request, 'PCBArtifactUpload.html', {'form': form, 'pcbs': pcbs})






#======================================================================================================================================================================================================================================================================================
from django.shortcuts import render, redirect, get_object_or_404
from .models import PCBOrderDetailsUpload
from .forms import PCBOrderDetailsUploadForm

def PCBOrderDetailsUpload_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        pcb_id = request.POST.get('PCBID')
        print('action', action)
        print('pcb_id', pcb_id)

        if action == 'insert':
            form = PCBOrderDetailsUploadForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('PCBOrderDetailsUpload')

        if action == 'update':
            instance = get_object_or_404(PCBOrderDetailsUpload, PCBID=pcb_id)
            form = PCBOrderDetailsUploadForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('PCBOrderDetailsUpload')

        if action == 'delete':
            instance = get_object_or_404(PCBOrderDetailsUpload, PCBID=pcb_id)
            instance.delete()
            return redirect('PCBOrderDetailsUpload')

    form = PCBOrderDetailsUploadForm()
    data = PCBOrderDetailsUpload.objects.all()
    return render(request, 'PCBOrderDetailsUpload.html', {'form': form, 'data': data})


#======================================================================================================================================================================================================================================================================================
from django.shortcuts import render, redirect, get_object_or_404
from .models import MechanicalDrawingUpload
from .forms import MechanicalDrawingUploadForm

def MechanicalDrawingUpload_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        mech_id = request.POST.get('MECHID')
        print('action', action)
        print('mech_id', mech_id)

        if action == 'insert':
            form = MechanicalDrawingUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('MechanicalDrawingUpload')

        if action == 'update':
            instance = get_object_or_404(MechanicalDrawingUpload, MECHID=mech_id)
            form = MechanicalDrawingUploadForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('MechanicalDrawingUpload')

        if action == 'delete':
            instance = get_object_or_404(MechanicalDrawingUpload, MECHID=mech_id)
            instance.delete()
            return redirect('MechanicalDrawingUpload')

    form = MechanicalDrawingUploadForm()
    data = MechanicalDrawingUpload.objects.all()
    return render(request, 'MechanicalDrawingUpload.html', {'form': form, 'data': data})



#======================================================================================================================================================
from django.shortcuts import render, redirect, get_object_or_404
from .models import MechBOMUpload
from .forms import MechBOMUploadForm

def MechBOMUpload_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        mech_id = request.POST.get('MECHID')
        print('action', action)
        print('mech_id', mech_id)

        if action == 'insert':
            form = MechBOMUploadForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('MechBOMUpload')

        if action == 'update':
            instance = get_object_or_404(MechBOMUpload, MECHID=mech_id)
            form = MechBOMUploadForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('MechBOMUpload')

        if action == 'delete':
            instance = get_object_or_404(MechBOMUpload, MECHID=mech_id)
            instance.delete()
            return redirect('MechBOMUpload')

    form = MechBOMUploadForm()
    data = MechBOMUpload.objects.all()
    return render(request, 'MechBOMUpload.html', {'form': form, 'data': data})


#======================================================================================================================================================================================================================================================================================
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import GSTR2B
import pandas as pd


def bulk_insert_gstr2b(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'bulk_insert':
            try:
                # Get the uploaded file
                file = request.FILES['file']
                data = pd.read_excel(file)

                # Map and sanitize data
                records = []
                for _, row in data.iterrows():
                    try:
                        invoice_date = pd.to_datetime(row['Unnamed: 4'], errors='coerce')  # Handle invalid dates
                        filing_date = pd.to_datetime(row['GSTR-1/IFF/GSTR-5 Filing Date'], errors='coerce')

                        # Skip rows with invalid dates
                        if pd.isna(invoice_date) or pd.isna(filing_date):
                            continue

                        record = GSTR2B(
                            gstin_supplier=row['GSTIN of supplier'],
                            trade_name=row['Trade/Legal name'],
                            invoice_number=row['Invoice Details'],
                            invoice_type=row['Unnamed: 3'],
                            invoice_date=invoice_date,
                            invoice_value=row['Unnamed: 5'],
                            place_of_supply=row['Place of supply'],
                            supply_reverse_charge=row['Supply Attract Reverse Charge'],
                            rate=row['Rate(%)'],
                            taxable_value=row['Taxable Value (₹)'],
                            integrated_tax=row['Tax Amount'],
                            central_tax=row['Unnamed: 11'],
                            state_ut_tax=row['Unnamed: 12'],
                            cess=row['Unnamed: 13'],
                            gstr_period=row['GSTR-1/IFF/GSTR-5 Period'],
                            gstr_filing_date=filing_date,
                            itc_availability=row['ITC Availability']
                        )
                        records.append(record)
                    except KeyError as e:
                        print(f"Missing column in data: {e}")
                    except Exception as e:
                        print(f"Error processing row: {e}")

                # Bulk insert records into the database
                if records:
                    GSTR2B.objects.bulk_create(records)

                return redirect('gstr2b')
            except Exception as e:
                print(f"Error occurred: {e}")
                
                return HttpResponse(f"An error occurred: {e}", status=500)

        # Handle filtering by trade_name
        elif 'trade_name' in request.POST:
            trade_name = request.POST.get('trade_name')
            filtered_records = GSTR2B.objects.filter(trade_name=trade_name).values()
            return JsonResponse({'records': list(filtered_records)})

    # Fetch all distinct trade names for the dropdown
    gstr2b_records = GSTR2B.objects.values('trade_name').distinct()
    return render(request, 'GSTR2B.html', {'gstr2b_records': gstr2b_records})


# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from .models import GSTR2B
# import pandas as pd

# def bulk_insert_gstr2b(request):
#     if request.method == 'POST':
#         try:
#             # Get the uploaded file
#             file = request.FILES['file']
#             data = pd.read_excel(file)

#             # Map and sanitize data
#             records = []
#             for _, row in data.iterrows():
#                 try:
#                     invoice_date = pd.to_datetime(row['Unnamed: 4'], errors='coerce')  # Handle invalid dates
#                     filing_date = pd.to_datetime(row['GSTR-1/IFF/GSTR-5 Filing Date'], errors='coerce')

#                     # Skip rows with invalid dates
#                     if pd.isna(invoice_date) or pd.isna(filing_date):
#                         continue

#                     record = GSTR2B(
#                         gstin_supplier=row['GSTIN of supplier'],
#                         trade_name=row['Trade/Legal name'],
#                         invoice_number=row['Invoice Details'],
#                         invoice_type=row['Unnamed: 3'],
#                         invoice_date=invoice_date,
#                         invoice_value=row['Unnamed: 5'],
#                         place_of_supply=row['Place of supply'],
#                         supply_reverse_charge=row['Supply Attract Reverse Charge'],
#                         rate=row['Rate(%)'],
#                         taxable_value=row['Taxable Value (₹)'],
#                         integrated_tax=row['Tax Amount'],
#                         central_tax=row['Unnamed: 11'],
#                         state_ut_tax=row['Unnamed: 12'],
#                         cess=row['Unnamed: 13'],
#                         gstr_period=row['GSTR-1/IFF/GSTR-5 Period'],
#                         gstr_filing_date=filing_date,
#                         itc_availability=row['ITC Availability']
#                     )
#                     records.append(record)
#                 except KeyError as e:
#                     # Log and handle missing columns
#                     print(f"Missing column in data: {e}")
#                 except Exception as e:
#                     # Log any unexpected errors
#                     print(f"Error processing row: {e}")

#             # Bulk insert records into the database
#             if records:
#                 GSTR2B.objects.bulk_create(records)

#             return JsonResponse({"message": f"{len(records)} records inserted successfully."})
#         except Exception as e:
#             # Log the error for debugging
#             print(f"Error occurred: {e}")
#             return HttpResponse(f"An error occurred: {e}", status=500)

#     # Fetch all records for display
#     gstr2b_records = GSTR2B.objects.all()
#     return render(request, 'GSTR2B.html', {'gstr2b_records': gstr2b_records})


#======================================================================================================================================================================================================================================================================================




#======================================================================================================================================================================================================================================================================================






#======================================================================================================================================================================================================================================================================================



