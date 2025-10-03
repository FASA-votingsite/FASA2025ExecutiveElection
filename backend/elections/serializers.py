from rest_framework import serializers
from .models import Election, Position, Candidate

class CandidateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_department = serializers.CharField(source='student.department', read_only=True)
    
    class Meta:
        model = Candidate
        fields = ['id', 'student', 'student_name', 'student_department', 'manifesto', 'photo', 'position']

class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'description', 'order', 'candidates']

class ElectionSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_active', 'positions']