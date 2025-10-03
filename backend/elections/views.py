from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Election, Position, Candidate
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer

@api_view(['GET'])
@permission_classes([])
def election_list(request):
    try:
        elections = Election.objects.filter(is_active=True)
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([])
def position_list(request):
    try:
        positions = Position.objects.filter(election__is_active=True)
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([])
def candidate_list(request):
    try:
        # Use select_related to optimize database queries
        candidates = Candidate.objects.filter(
            position__election__is_active=True
        ).select_related('student', 'position', 'position__election')
        
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in candidate_list: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': 'Internal server error in candidates'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )