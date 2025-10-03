from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Vote
from elections.models import Candidate, Position

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cast_vote(request):
    candidate_id = request.data.get('candidate_id')
    position_id = request.data.get('position_id')
    
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        position = Position.objects.get(id=position_id)
        
        # Check if user has already voted for this position
        if Vote.objects.filter(voter=request.user, position=position).exists():
            return Response(
                {'error': 'You have already voted for this position'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the vote
        vote = Vote.objects.create(
            voter=request.user,
            position=position,
            candidate=candidate
        )
        
        return Response({
            'message': 'Vote cast successfully!',
            'vote_id': vote.id
        })
        
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
    except Position.DoesNotExist:
        return Response({'error': 'Position not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vote_list(request):
    votes = Vote.objects.filter(voter=request.user)
    data = []
    for vote in votes:
        data.append({
            'id': vote.id,
            'position': vote.position.title,
            'candidate': vote.candidate.student.get_full_name(),
            'timestamp': vote.timestamp
        })
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def election_results(request):
    # For now, let any authenticated user see results
    # Later we can restrict to admin only
    from collections import defaultdict
    from django.db.models import Count
    
    # Get all positions with their candidates and vote counts
    positions = Position.objects.filter(election__is_active=True)
    results = []
    
    for position in positions:
        position_data = {
            'position_id': position.id,
            'position_title': position.title,
            'candidates': []
        }
        
        # Get vote counts for each candidate in this position
        vote_counts = Vote.objects.filter(position=position).values(
            'candidate'
        ).annotate(
            total_votes=Count('candidate')
        )
        
        # Create a dictionary of candidate_id -> vote_count
        vote_dict = {item['candidate']: item['total_votes'] for item in vote_counts}
        
        for candidate in position.candidates.all():
            position_data['candidates'].append({
                'candidate_id': candidate.id,
                'candidate_name': candidate.student.get_full_name(),
                'votes': vote_dict.get(candidate.id, 0)
            })
        
        results.append(position_data)
    
    return Response(results)