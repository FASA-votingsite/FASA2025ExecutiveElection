from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import FacultyUser
# Create your views here.


@api_view(['POST'])
@permission_classes([])  # Allow unauthenticated access for login
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
    request.user.auth_token.delete()
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