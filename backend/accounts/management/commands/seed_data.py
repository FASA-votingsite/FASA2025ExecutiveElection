from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import FacultyUser
from elections.models import Election, Position, Candidate

class Command(BaseCommand):
    help = 'Seed initial data for testing'
    
    def handle(self, *args, **options):
        # Create test students
        try:
            student1 = FacultyUser.objects.create_user(
                matric_number='ART/20/001',
                email='student1@uniben.edu',
                first_name='John',
                last_name='Doe',
                department='Fine Arts',
                password='password123'
            )
            
            student2 = FacultyUser.objects.create_user(
                matric_number='ART/20/002',
                email='student2@uniben.edu',
                first_name='Jane',
                last_name='Smith',
                department='Music',
                password='password123'
            )
            
            student3 = FacultyUser.objects.create_user(
                matric_number='ART/20/003',
                email='student3@uniben.edu',
                first_name='Mike',
                last_name='Johnson',
                department='Theatre Arts',
                password='password123'
            )
            
            student4 = FacultyUser.objects.create_user(
                matric_number='ART/20/004',
                email='student4@uniben.edu',
                first_name='Sarah',
                last_name='Williams',
                department='Linguistics',
                password='password123'
            )
            
            # Create election with start and end dates
            election = Election.objects.create(
                title='2024 Faculty of Art Executive Elections',
                description='Annual elections for faculty executive positions',
                start_date=timezone.now() - timedelta(days=1),  # Started yesterday
                end_date=timezone.now() + timedelta(days=7),    # Ends in 7 days
                is_active=True
            )
            
            # Create positions
            president = Position.objects.create(
                election=election,
                title='President',
                description='Faculty President - Head of the student executive council',
                order=1
            )
            
            vice_president = Position.objects.create(
                election=election,
                title='Vice President',
                description='Assists the President and acts in their absence',
                order=2
            )
            
            secretary = Position.objects.create(
                election=election,
                title='Secretary',
                description='Handles correspondence and meeting minutes',
                order=3
            )
            
            # Create candidates for President
            Candidate.objects.create(
                position=president,
                student=student1,
                manifesto='I will represent all students effectively and ensure our voices are heard!'
            )
            
            Candidate.objects.create(
                position=president,
                student=student2,
                manifesto='Together we can make a difference in our faculty!'
            )
            
            # Create candidates for Vice President
            Candidate.objects.create(
                position=vice_president,
                student=student3,
                manifesto='I will support the President and ensure smooth operations'
            )
            
            # Create candidate for Secretary
            Candidate.objects.create(
                position=secretary,
                student=student4,
                manifesto='I will ensure transparent communication and accurate records'
            )
            
            self.stdout.write(self.style.SUCCESS('Successfully seeded test data'))
            self.stdout.write(self.style.SUCCESS('Test students created:'))
            self.stdout.write(f'  - {student1.matric_number}: {student1.get_full_name()}')
            self.stdout.write(f'  - {student2.matric_number}: {student2.get_full_name()}')
            self.stdout.write(f'  - {student3.matric_number}: {student3.get_full_name()}')
            self.stdout.write(f'  - {student4.matric_number}: {student4.get_full_name()}')
            self.stdout.write(self.style.SUCCESS('Election created with 3 positions and 4 candidates'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding data: {e}'))