from django.urls import path
from . import views
from .bulk_upload import bulk_upload_students

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('profile/', views.student_profile, name='student_profile'),
    # Remove the register endpoints for now to avoid errors
    # path('register/', views.register_student, name='register_student'),
    # path('bulk-register/', views.bulk_register_students, name='bulk_register_students'),
    path('admin/bulk-upload/', bulk_upload_students, name='bulk_upload_students'),
    path('admin/download-sample-csv/', views.download_sample_csv, name='download_sample_csv'),
]