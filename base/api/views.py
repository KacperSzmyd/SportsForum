from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from base.api.serializers import RoomSerializer, UserMiniSerializer, UserSerializer
from base.models import Room, User


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RoomSerializer


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
            return Response({'Access': 'denied'})
