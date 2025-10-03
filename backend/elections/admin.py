from django.contrib import admin
from .models import Election, Position, Candidate
# Register your models here.


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'description')
    inlines = [PositionInline]

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'election', 'order')
    list_filter = ('election',)
    search_fields = ('title', 'description')
    inlines = [CandidateInline]

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('student', 'position', 'created_at')
    list_filter = ('position__election', 'position')
    search_fields = ('student_first_name', 'studentlast_name', 'student_matric_number')