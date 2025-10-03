import os
from datetime import datetime
from django.db import models
from accounts.models import FacultyUser

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.title
    
    class Meta:
        ordering = ['-start_date']

class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    def _str_(self):
        return f"{self.election.title} - {self.title}"
    
    class Meta:
        ordering = ['order', 'title']



class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    student = models.ForeignKey(FacultyUser, on_delete=models.CASCADE)
    manifesto = models.TextField(blank=True)
    photo = models.ImageField(upload_to='candidates/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.student.get_full_name()} - {self.position.title}"
    
    class Meta:
        unique_together = ['position', 'student']
    
    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return None
    

