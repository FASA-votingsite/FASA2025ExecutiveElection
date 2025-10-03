from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import FacultyUser

@api_view(['POST'])
@permission_classes([])
def student_login(request):
    matric_number = request.data.get('matric_number')
    password = request.data.get('password')
    
    try:
        user = FacultyUser.objects.get(matric_number=matric_number)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'matric_number': user.matric_number,
                    'full_name': user.get_full_name(),
                    'department': user.department,
                    'has_voted': user.has_voted
                }
            })
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    except FacultyUser.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def student_logout(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': 'Successfully logged out'})

@api_view(['GET'])
def student_profile(request):
    user = request.user
    return Response({
        'id': user.id,
        'matric_number': user.matric_number,
        'full_name': user.get_full_name(),
        'department': user.department,
        'has_voted': user.has_voted
    })

# ADD THE MISSING FUNCTIONS:

@api_view(['POST'])
@permission_classes([])
def register_student(request):
    """Register a new student (for admin use or bulk import)"""
    matric_number = request.data.get('matric_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    department = request.data.get('department')
    password = request.data.get('password', 'FASA@2025student')
    
    if not all([matric_number, first_name, last_name, department]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if FacultyUser.objects.filter(matric_number=matric_number).exists():
        return Response({'error': 'Student with this matric number already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        student = FacultyUser.objects.create_user(
            matric_number=matric_number,
            first_name=first_name,
            last_name=last_name,
            department=department,
            password=password
        )
        
        return Response({
            'message': 'Student registered successfully',
            'student': {
                'id': student.id,
                'matric_number': student.matric_number,
                'full_name': student.get_full_name(),
                'department': student.department
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([])
def bulk_register_students(request):
    """Bulk register students from a list"""
    students_data = request.data.get('students', [])
    
    if not students_data:
        return Response({'error': 'No student data provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    created_students = []
    errors = []
    
    for student_data in students_data:
        try:
            if FacultyUser.objects.filter(matric_number=student_data['matric_number']).exists():
                errors.append(f"Student {student_data['matric_number']} already exists")
                continue
            
            student = FacultyUser.objects.create_user(
                matric_number=student_data['matric_number'],
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                department=student_data['department'],
                password=student_data.get('password', 'defaultpassword123')
            )
            
            created_students.append({
                'matric_number': student.matric_number,
                'full_name': student.get_full_name(),
                'department': student.department
            })
            
        except Exception as e:
            errors.append(f"Error creating {student_data.get('matric_number', 'unknown')}: {str(e)}")
    
    return Response({
        'created': created_students,
        'errors': errors,
        'message': f'Created {len(created_students)} students, {len(errors)} errors'
    })

def download_sample_csv(request):
    # Create a sample CSV file
    csv_content = """matric_number,first_name,last_name,department
ART2201394,Favour,Egharevba,Philosophy
ART2309155,ADEBAYO, FISAYO, Foreign Languages
ART2200753,ADAUDO, AGATHA,History & InternationalStudies
ART2200752,ABUGU, CHIOMA,History & InternationalStudies
ART2200753,ADAUDO, AGATHA ,History & InternationalStudies"""
    
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'
    return response