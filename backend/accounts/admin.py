from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FacultyUser
# Register your models here.


class FacultyUserAdmin(UserAdmin):
    model = FacultyUser
    list_display = ('matric_number', 'email', 'first_name', 'last_name', 'department', 'has_voted', 'is_staff')
    list_filter = ('department', 'has_voted', 'is_staff')
    fieldsets = (
        (None, {'fields': ('matric_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Voting Status', {'fields': ('has_voted',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matric_number', 'email', 'first_name', 'last_name', 'department', 'password1', 'password2'),
        }),
    )
    search_fields = ('matric_number', 'first_name', 'last_name', 'email')
    ordering = ('matric_number',)

admin.site.register(FacultyUser, FacultyUserAdmin)