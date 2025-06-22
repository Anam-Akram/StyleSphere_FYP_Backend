from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from User.serializers import UserCreateSerializer
from User.models import UserAccount

@api_view(['POST'])
@permission_classes([AllowAny])
def get_tailor_data(request):
    try:
        tailor_id = request.data.get('id')
        if not tailor_id:
            return Response(
                {"message": "ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = UserAccount.objects.get(id=tailor_id)
        serializer = UserCreateSerializer(user_data)
        return Response(
            {"message": "Tailor data retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    except UserAccount.DoesNotExist:
        return Response(
            {"message": "Tailor not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"message": "An error occurred.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['POST'])
@permission_classes([AllowAny])
def get_tailors_data(request):
    try:
        user_data = UserAccount.objects.filter(is_tailor=True)
        serializer = UserCreateSerializer(user_data,many=True)
        return Response(
            {"message": "Tailor data retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"message": "An error occurred.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )