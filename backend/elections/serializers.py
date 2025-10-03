from rest_framework import serializers
from .models import Election, Position, Candidate

class CandidateSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_department = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()  # Add this

    class Meta:
        model = Candidate
        fields = ['id', 'student', 'student_name', 'student_department', 'manifesto', 'photo', 'photo_url', 'position']

    def get_student_name(self, obj):
        return obj.student.get_full_name()

    def get_student_department(self, obj):
        return obj.student.department

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

# ... rest of your serializers ...

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