import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings')
django.setup()

from accounts.models import FacultyUser
from elections.models import Election, Position, Candidate

def create_election():
    print("Creating election data...")
    
    # Create an active election
    election = Election.objects.create(
        title="2024 Faculty of Art Executive Elections",
        description="Annual elections for faculty executive positions",
        start_date=timezone.now() - timedelta(days=1),
        end_date=timezone.now() + timedelta(days=7),
        is_active=True  # THIS IS CRITICAL!
    )
    print(f"Created election: {election.title}")
    
    # Create positions
    positions_data = [
        {'title': 'President', 'description': 'Head of student executive council', 'order': 1},
        {'title': 'Vice President', 'description': 'Assists the President', 'order': 2},
        {'title': 'Secretary', 'description': 'Handles correspondence', 'order': 3},
    ]
    
    positions = []
    for data in positions_data:
        position = Position.objects.create(
            election=election,
            title=data['title'],
            description=data['description'],
            order=data['order']
        )
        positions.append(position)
        print(f"Created position: {position.title}")
    
    # Get or create test students
    students_data = [
        {'matric': 'ART/20/001', 'first': 'John', 'last': 'Doe', 'dept': 'Fine Arts'},
        {'matric': 'ART/20/002', 'first': 'Jane', 'last': 'Smith', 'dept': 'Music'},
        {'matric': 'ART/20/003', 'first': 'Mike', 'last': 'Johnson', 'dept': 'Theatre Arts'},
    ]
    
    students = []
    for data in students_data:
        student, created = FacultyUser.objects.get_or_create(
            matric_number=data['matric'],
            defaults={
                'email': f"{data['matric']}@uniben.edu",
                'first_name': data['first'],
                'last_name': data['last'],
                'department': data['dept'],
            }
        )
        if created:
            student.set_password('password123')
            student.save()
            print(f"Created student: {data['matric']}")
        students.append(student)
    
    # Create candidates
    candidates_data = [
        {'position': positions[0], 'student': students[0], 'manifesto': 'I will represent all students effectively!'},
        {'position': positions[0], 'student': students[1], 'manifesto': 'Together we can make a difference!'},
        {'position': positions[1], 'student': students[2], 'manifesto': 'I will support the President!'},
    ]
    
    for data in candidates_data:
        candidate = Candidate.objects.create(
            position=data['position'],
            student=data['student'],
            manifesto=data['manifesto']
        )
        print(f"Created candidate: {data['student'].get_full_name()} for {data['position'].title}")
    
    print("\nElection data created successfully!")
    print("Test login: ART/20/001 / password123")

if __name__ == '__main__':
    create_election()