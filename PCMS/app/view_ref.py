from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from openpyxl import Workbook
from io import BytesIO
import pandas as pd
from .models import tblProject

def tblProject_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        project_id = request.POST.get('project_id')
        print(project_id)

        if action == 'insert':
            new_project = tblProject(
                company_name=request.POST.get('company_name'),
                company_code=request.POST.get('company_code'),
                project_name1=request.POST.get('project_name1'),
                project_code1=request.POST.get('project_code1'),
                projcode_partnumber=request.POST.get('projcode_partnumber'),
                projcode_partname=request.POST.get('projcode_partname')
            )
            new_project.save()
            return redirect('tblProject')

        elif action == 'update':
            project = get_object_or_404(tblProject, id=project_id)
            project.company_name = request.POST.get('company_name')
            project.company_code = request.POST.get('company_code')
            project.project_name1 = request.POST.get('project_name1')
            project.project_code1 = request.POST.get('project_code1')
            project.projcode_partnumber = request.POST.get('projcode_partnumber')
            project.projcode_partname = request.POST.get('projcode_partname')
            project.save()
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

            file_extension = xlsx_file.name.split('.')[-1]
            if file_extension != 'xlsx':
                return HttpResponse("Unsupported File Format", status=400)

            try:
                df = pd.read_excel(xlsx_file, engine='openpyxl', dtype=str)  # Read all data as strings

                # Define a mapping of Excel file columns to your expected model fields
                column_mapping = {
                    'Company Name': 'company_name',
                    'Company Code': 'company_code',
                    'Project Name1': 'project_name1',
                    'ProjectCode1': 'project_code1',
                    'ProjCode- Partnumber': 'projcode_partnumber',
                    'ProjCode-Partname': 'projcode_partname',
                }

                # Check if all required columns are present in the uploaded file
                if not set(column_mapping.keys()).issubset(df.columns.str.strip()):
                    missing_cols = set(column_mapping.keys()) - set(df.columns.str.strip())
                    return HttpResponse(f"Error: Missing columns in the file: {missing_cols}", status=400)

                # Rename the columns according to the mapping
                df = df.rename(columns=column_mapping)

                for _, row in df.iterrows():
                    tblProject.objects.update_or_create(
                        company_code=row['company_code'],
                        defaults={
                            'company_name': row['company_name'],
                            'project_name1': row['project_name1'],
                            'project_code1': row['project_code1'],
                            'projcode_partnumber': row['projcode_partnumber'],
                            'projcode_partname': row['projcode_partname'],
                        }
                    )

                return redirect('tblProject')  # Redirect to the desired page after successful bulk insert

            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=500)

        elif action == 'download_project_details':
            try:
                wb = Workbook()
                ws = wb.active
                ws.title = "Project Details"
                headers = ['Company Name', 'Company Code', 'Project Name', 'Project Code', 'Part Number', 'Part Name']
                ws.append(headers)

                data = tblProject.objects.all()
                for obj in data:
                    ws.append([
                        obj.company_name, obj.company_code, obj.project_name1, 
                        obj.project_code1, obj.projcode_partnumber, obj.projcode_partname
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

            except Exception as e:
                return HttpResponse("Error generating Excel.", status=500)

    search_query = request.GET.get('search', '')
    project_data = tblProject.objects.all()

    if search_query:
        project_data = project_data.filter(project_name1__icontains=search_query) | project_data.filter(
            company_name__icontains=search_query
        ) | project_data.filter(
            projcode_partname__icontains=search_query
        )

    paginator = Paginator(project_data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tblProject.html', {'project_data': page_obj, 'search_query': search_query})