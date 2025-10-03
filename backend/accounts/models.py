from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class FacultyUserManager(BaseUserManager):
    def create_user(self, matric_number, first_name, last_name, department, password=None, **extra_fields):
        if not matric_number:
            raise ValueError('The Matric Number must be set')
        
        
        user = self.model(
            matric_number=matric_number,
            first_name=first_name,
            last_name=last_name,
            department=department,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_number, first_name, last_name, department, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(matric_number, first_name, last_name, department, password, **extra_fields)

class FacultyUser(AbstractUser):
    username = None
    matric_number = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)
    has_voted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'matric_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department']
    
    objects = FacultyUserManager()
    
    def _str_(self):
        return f"{self.matric_number} - {self.get_full_name()}"

    class Meta:
        verbose_name = "Faculty User"
        verbose_name_plural = "Faculty Users"