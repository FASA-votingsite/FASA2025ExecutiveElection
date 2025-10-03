from django.test import TestCase

# Create your tests here.
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings')
django.setup()

from elections.models import Candidate
from elections.serializers import CandidateSerializer

try:
    candidates = Candidate.objects.filter(position_election_is_active=True)
    print(f"Found {candidates.count()} candidates")
    
    for candidate in candidates:
        print(f"Candidate: {candidate.student.get_full_name()}")
        print(f"Position: {candidate.position.title}")
        print(f"Election active: {candidate.position.election.is_active}")
        
    # Test serialization
    serializer = CandidateSerializer(candidates, many=True)
    print("Serialization successful")
    print(serializer.data)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()