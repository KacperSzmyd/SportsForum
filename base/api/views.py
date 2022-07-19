from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from base.api.serializers import RoomSerializer, UserMiniSerializer, UserSerializer, MessageSerializer
from base.models import Room, User, Topic, Message


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        topic = Topic.objects.create(name=request.data['topic'])
        room = Room.objects.create(host=request.user, topic=topic,
                                   name=request.data['name'], description=request.data['description'])
        room.participants.add(request.user)
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        if request.user.is_authenticated and request.data.get('message'):
            message = Message.objects.create(user=request.user, body=request.data['message'], room=room)
            message.save()

        if request.data.get('topic'):
            topic, created = Topic.objects.get_or_create(name=request.data['topic'])
            room.topic = topic

        room.description = request.data.get('description', room.description)
        room.name = request.data.get('name', room.name)
        room.save()
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def messages(self, request, *args, **kwargs):
        # get room
        queryset = self.get_object()
        # messages = dict(enumerate([(msg.user.username, msg.body) for msg in queryset.message_set.all()], start=1))
        messages = queryset.message_set.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserMiniSerializer

    @action(detail=True, methods=['GET'])
    def info(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.is_authenticated and request.user == user:
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)

        else:
            raise PermissionDenied()
