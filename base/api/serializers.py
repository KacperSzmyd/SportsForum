from rest_framework.serializers import ModelSerializer

from base.models import Room, User


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['host', 'topic', 'name', 'description', 'participants', 'created', 'last_action']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'rooms']


class UserMiniSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']