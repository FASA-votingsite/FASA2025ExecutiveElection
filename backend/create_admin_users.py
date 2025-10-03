import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings')
django.setup()

from accounts.models import FacultyUser

def create_admin_users():
    admins = [
        {
            'matric_number': 'ADMIN001',
            'first_name': 'Dean',
            'last_name': 'Faculty of Art',
            'department': 'Administration',
            'password': 'FASA@2025admin',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'matric_number': 'ADMIN002', 
            'first_name': 'Election',
            'last_name': 'Coordinator',
            'department': 'Administration',
            'password': 'FASA@2025admin',
            'is_staff': True,
            'is_superuser': True
        }
    ]
    
    for admin_data in admins:
        if not FacultyUser.objects.filter(matric_number=admin_data['matric_number']).exists():
            admin = FacultyUser.objects.create_superuser(
                matric_number=admin_data['matric_number'],
                first_name=admin_data['first_name'],
                last_name=admin_data['last_name'],
                department=admin_data['department'],
                password=admin_data['password']
            )
            print(f"✅ Created admin: {admin_data['matric_number']} - {admin.get_full_name()}")
        else:
            print(f"Admin {admin_data['matric_number']} already exists")

if __name__ == '__main__':
    create_admin_users()