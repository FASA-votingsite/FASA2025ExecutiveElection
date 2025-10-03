from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Vote
from elections.models import Candidate, Position

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vote_list(request):
    try:
        votes = Vote.objects.filter(voter=request.user)
        data = []
        for vote in votes:
            data.append({
                'position': vote.position.title,
                'candidate': vote.candidate.student.get_full_name(),
                'timestamp': vote.timestamp
            })
        return Response(data)
    except Exception as e:
        print(f"Error in vote_list: {str(e)}")
        return Response([], status=status.HTTP_200_OK)  # Return empty list instead of error

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
            return Response({'error': 'You have already voted for this position'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the vote
        vote = Vote.objects.create(
            voter=request.user,
            position=position,
            candidate=candidate
        )
        
        # Update user's has_voted status
        request.user.has_voted = True
        request.user.save()
        
        return Response({
            'message': 'Vote cast successfully!',
            'vote_id': vote.id
        })
        
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
    except Position.DoesNotExist:
        return Response({'error': 'Position not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error in cast_vote: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def election_results(request):
    try:
        # Simple implementation for now
        return Response([])
    except Exception as e:
        print(f"Error in election_results: {str(e)}")
        return Response([], status=status.HTTP_200_OK)