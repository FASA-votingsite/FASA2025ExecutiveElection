from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Election, Position, Candidate
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer

@api_view(['GET'])
@permission_classes([])  # Allow unauthenticated access
def election_list(request):
    try:
        elections = Election.objects.filter(is_active=True)
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([])  # Allow unauthenticated access
def position_list(request):
    try:
        positions = Position.objects.filter(election__is_active=True)
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([])  # Allow unauthenticated access
def candidate_list(request):
    try:
        candidates = Candidate.objects.filter(position_election_is_active=True)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)