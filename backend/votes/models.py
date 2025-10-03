from django.db import models
from accounts.models import FacultyUser
from elections.models import Candidate, Position
# Create your models here.


class Vote(models.Model):
    voter = models.ForeignKey(FacultyUser, on_delete=models.CASCADE, related_name='votes')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.voter.matric_number} voted for {self.candidate.student.get_full_name()}"
    
    class Meta:
        unique_together = ('voter', 'position')
        ordering = ['-timestamp']