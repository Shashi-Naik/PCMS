import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import tblVendordetails, tblProject, tblPartNumber

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


from .models import CreateVendor,CreateCustomer,CreateProject,UploadInvoicefromVendor
from .forms import CreateVendorForm,CreateCustomerForm,CreateProjectForm,UploadInvoicefromVendorForm
from django.shortcuts import render, redirect, get_object_or_404
def CreateVendor_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        vendor_id = request.POST.get('vendor_id')

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

    else:
        form = CreateVendorForm()
        vendors = CreateVendor.objects.all()
    
    return render(request, 'vendordetails.html', {
        'form': form,
        'vendors': vendors
    })
    
    
#--------------------------------------------------------------------------------------

def CreateCustomer_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        customer_id = request.POST.get('customer_id')

        if action == 'insert':
            form = CreateCustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CreateCustomer')

        elif action == 'update':
            vendor = get_object_or_404(CreateCustomer, CUSTID=customer_id)
            form = CreateCustomerForm(request.POST, instance=vendor)
            if form.is_valid():
                form.save()
                return redirect('CreateCustomer')

        elif action == 'delete':
            vendor = get_object_or_404(CreateCustomer, CUSTID=customer_id)
            vendor.delete()
            return redirect('CreateCustomer')

    else:
        form = CreateCustomerForm()
        custr = CreateCustomer.objects.all()
    
    return render(request, 'CreateCustomer.html', {
        'form': form,
        'custr': custr
    })
    
#------------------------------------------------------------------------------


def CreateProject_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        project_id =request.POST.get('project_id')
        
        if action == 'insert':
            form = CreateProjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CreateProject')
        elif action == 'update':
            pjt = get_object_or_404(CreateProject, PROJID=project_id)
            form = CreateProjectForm(request.POST, instance=pjt)    
            if form.is_valid():
                form.save()
                return redirect('CreateProject')
        elif action == 'delete':
            pjt = get_object_or_404(CreateProject,PROJID=project_id)  
            pjt.delete()  
            return redirect('CreateProject')
    
    else:
        form = CreateProjectForm()
        pjt = CreateProject.objects.all()
    
    return render(request, 'CreateProject.html',{'form': form,'pjt':pjt})

#-------------------------------------------------------------------------



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UploadInvoicefromVendor,CreateInvoiceBasedPartNumber,CreatePurchaseBasedCosting
from .forms import UploadInvoicefromVendorForm,CreateInvoiceBasedPartNumberForm,CreatePurchaseBasedCostingForm

def UploadInvoicefromVendor_view(request):
    form = UploadInvoicefromVendorForm()
    data = UploadInvoicefromVendor.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        Vendor_id = request.POST.get('vendor_id')  # Changed to match the hidden field in HTML
        
        try:
            if action == 'insert':
                form = UploadInvoicefromVendorForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Invoice added successfully.')
                else:
                    messages.error(request, 'Error adding invoice. Please correct the form errors.')

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

            else:
                messages.error(request, 'Invalid action.')

            return redirect('UploadInvoicefromVendor')

        except UploadInvoicefromVendor.DoesNotExist:
            messages.error(request, 'Invoice not found for the specified Vendor ID.')
            return redirect('UploadInvoicefromVendor')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('UploadInvoicefromVendor')

    context = {
        'form': form,
        'data': data
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
                    messages.success(request, 'Invoice added successfully.')
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CreatePurchaseBasedCostingForm
from .models import CreatePurchaseBasedCosting

def CreatePurchaseBasedCosting_view(request):
    form = CreatePurchaseBasedCostingForm()
    data = CreatePurchaseBasedCosting.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        cost_id = request.POST.get('cost_id')

        try:
            if action == 'insert':
                form = CreatePurchaseBasedCostingForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Record added successfully to Purchase-Based Costing.')
                else:
                    messages.error(request, 'Error adding record. Please correct the form errors.')

            elif action == 'update':
                data_instance = get_object_or_404(CreatePurchaseBasedCosting, COSTID=cost_id)
                form = CreatePurchaseBasedCostingForm(request.POST, instance=data_instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Record with COSTID {cost_id} updated successfully.')
                else:
                    messages.error(request, f'Error updating record with COSTID {cost_id}. Please correct the form errors.')

            elif action == 'delete':
                data_instance = get_object_or_404(CreatePurchaseBasedCosting, COSTID=cost_id)
                data_instance.delete()
                messages.success(request, f'Record with COSTID {cost_id} deleted successfully.')

            else:
                messages.error(request, 'Invalid action selected. Please choose a valid operation.')

            return redirect('CreatePurchaseBasedCosting')

        except CreatePurchaseBasedCosting.DoesNotExist:
            messages.error(request, f'Record with COSTID {cost_id} not found.')
            return redirect('CreatePurchaseBasedCosting')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('CreatePurchaseBasedCosting')

    context = {
        'form': form,
        'data': data
    }
    return render(request, 'CreatePurchaseBasedCosting.html', context)


#-------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReadPurchaseBasedCostingForm
from .models import ReadPurchaseBasedCosting

def ReadPurchaseBasedCosting_view(request):
    form = ReadPurchaseBasedCostingForm()
    data = ReadPurchaseBasedCosting.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        cost_id = request.POST.get('COSTID')

        try:
            if action == 'insert':
                form = ReadPurchaseBasedCostingForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Record added successfully to Purchase-Based Costing.')
                else:
                    messages.error(request, 'Error adding record. Please correct the form errors.')

            elif action == 'update':
                data_instance = get_object_or_404(ReadPurchaseBasedCosting, COSTID=cost_id)
                form = ReadPurchaseBasedCostingForm(request.POST, instance=data_instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Record with COSTID {cost_id} updated successfully.')
                else:
                    messages.error(request, f'Error updating record with COSTID {cost_id}. Please correct the form errors.')

            elif action == 'delete':
                data_instance = get_object_or_404(ReadPurchaseBasedCosting, COSTID=cost_id)
                data_instance.delete()
                messages.success(request, f'Record with COSTID {cost_id} deleted successfully.')

            else:
                messages.error(request, 'Invalid action selected. Please choose a valid operation.')

            return redirect('ReadPurchaseBasedCosting')

        except ReadPurchaseBasedCosting.DoesNotExist:
            messages.error(request, f'Record with COSTID {cost_id} not found.')
            return redirect('ReadPurchaseBasedCosting')

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('ReadPurchaseBasedCosting')

    context = {
        'form': form,
        'data': data
    }
    return render(request, 'ReadPurchaseBasedCosting.html', context)

#-------------------------------------------------------------------------