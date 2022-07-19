from rest_framework.serializers import ModelSerializer

from base.models import Room, User, Topic, Message


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class UserMiniSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class RoomSerializer(ModelSerializer):
    host = UserMiniSerializer(many=False, read_only=True)
    participants = UserMiniSerializer(many=True, read_only=True)
    topic = TopicSerializer(many=False)

    class Meta:
        model = Room
        fields = ['host', 'topic', 'name', 'description', 'participants', 'created', 'last_action']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'rooms']
        extra_kwargs = {'password': {'required': True, 'write_only': True}, 'email': {'required': True}}


class MessageSerializer(ModelSerializer):
    user = UserMiniSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['user', 'body', 'last_action']