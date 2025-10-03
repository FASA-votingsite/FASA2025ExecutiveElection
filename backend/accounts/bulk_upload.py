import csv
import io
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import FacultyUser

# Replace the @user_passes_test decorator with @staff_member_required
@staff_member_required
def bulk_upload_students(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Check if the file is a CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, '❌ Please upload a CSV file')
            return render(request, 'admin/bulk_upload.html')
        
        # Read the CSV file
        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
        except:
            messages.error(request, '❌ Error reading CSV file')
            return render(request, 'admin/bulk_upload.html')
        
        success_count = 0
        error_count = 0
        errors = []
        
        # Skip header row and process data
        reader = csv.reader(io_string, delimiter=',', quotechar='"')
        header = next(reader, None)  # Skip header
        
        # Validate header
        expected_header = ['matric_number', 'email', 'first_name', 'last_name', 'department']
        if header != expected_header:
            errors.append(f"❌ Invalid CSV format. Expected columns: {', '.join(expected_header)}")
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
            if len(row) < 5:
                errors.append(f"Row {row_num}: ❌ Insufficient data (need 5 columns)")
                error_count += 1
                continue
            
            try:
                matric_number, email, first_name, last_name, department = [field.strip() for field in row[:5]]
                
                # Validate required fields
                if not all([matric_number, email, first_name, last_name, department]):
                    errors.append(f"Row {row_num}: ❌ All fields are required")
                    error_count += 1
                    continue
                
                # Check if student already exists
                if FacultyUser.objects.filter(matric_number=matric_number).exists():
                    errors.append(f"Row {row_num}: ❌ Student {matric_number} already exists")
                    error_count += 1
                    continue
                
                # Create student
                student = FacultyUser.objects.create_user(
                    matric_number=matric_number,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    department=department,
                    password='defaultpassword123'  # Default password
                )
                success_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: ❌ Error: {str(e)}")
                error_count += 1
        
        # Show results
        if success_count > 0:
            messages.success(request, f'✅ Successfully imported {success_count} students!')
        if error_count > 0:
            messages.error(request, f'❌ Failed to import {error_count} students. Check errors below.')
        
        return render(request, 'admin/bulk_upload.html', {'errors': errors})
    
    return render(request, 'admin/bulk_upload.html')