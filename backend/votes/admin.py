from django.contrib import admin
from .models import Vote
# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'position', 'candidate', 'timestamp')
    list_filter = ('position__election', 'position')
    search_fields = ('voter_matric_number', 'voterfirst_name', 'voter_last_name')
    readonly_fields = ('timestamp',)