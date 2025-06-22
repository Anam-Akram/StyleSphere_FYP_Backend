from lib2to3.fixes.fix_input import context

from django.db import IntegrityError
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from chat.models import ChatRoom, ChatMessage

class ChatRoomView(APIView):
	permission_classes = [AllowAny]
	def get(self, request, userId):
		permission_classes = [AllowAny]
		chatRooms = ChatRoom.objects.filter(member=userId)
		serializer = ChatRoomSerializer(
			chatRooms, many=True, context={"request": request}
		)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		permission_classes = [AllowAny]
		# Retrieve the list of member IDs from the request data
		members = request.data.get('members')

		# Ensure that the members list is valid and contains at least 2 members
		if not members or len(members) < 2:
			return Response(
				{"message": "At least two members are required to create a chat room."},
				status=status.HTTP_400_BAD_REQUEST
			)

		# Sort the members list to ensure order doesn't matter in comparison
		member_ids = set(members)

		# Check for an existing room with the exact same members
		existing_room = ChatRoom.objects.filter(
			member__id__in=member_ids
		).distinct()

		# Further filter to ensure that the room has *exactly* the same members
		# A room must have no additional members or missing members
		existing_room = existing_room.filter(
			member__id__in=member_ids
		).prefetch_related('member')

		# Check if the room has the exact number of members
		for room in existing_room:
			room_member_ids = set(room.member.values_list('id', flat=True))
			if room_member_ids == member_ids:
				return Response(
					{
						"message": "Chat room already exists with the specified members.",
						"status": status.HTTP_200_OK,
						"data": ChatRoomSerializer(room).data
					}
				)

		# If no existing room is found, create a new room
		serializer = ChatRoomSerializer(data=request.data, context={"request": request})
		if serializer.is_valid():
			try:
				serializer.save()
				data = {
					"message": "Chat created successfully",
					"status": status.HTTP_200_OK,
					"data": serializer.data
				}
				return Response(data)
			except IntegrityError as e:
				return Response(
					{"message": "Error creating chat room", "error": str(e)},
					status=status.HTTP_400_BAD_REQUEST
				)

		# If the serializer is invalid, return the errors
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	# def post(self, request):
	# 	serializer = ChatRoomSerializer(
	# 		data=request.data, context={"request": request}
	# 	)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		data = {"message": "Chat created successfully",
	# 				"status" : status.HTTP_200_OK,
	# 				"data":serializer.data
	# 				}
	# 		return Response(data)
	# 	return Response(serializer.errors , {context: "not working"}, status=status.HTTP_400_BAD_REQUEST)

class MessagesView(ListAPIView):
	permission_classes = [AllowAny]
	serializer_class = ChatMessageSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		permission_classes = [AllowAny]
		roomId = self.kwargs['roomId']
		return ChatMessage.objects.\
			filter(chat__roomId=roomId).order_by('timestamp')
