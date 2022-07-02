from base.models import User, Topic, Message, Room
from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='dummy', email='dummy@emai.com', password='321Qwerty')
        self.user2 = User.objects.create_user(username='dummy2', email='dummy2@emai.com', password='321Qwerty')
        self.user3 = User.objects.create_user(username='dummy3', email='dummy3@emai.com', password='321Qwerty')

    def test_creating_users(self):
        self.assertEqual(str(self.user1), 'Dummy')
        self.assertEqual(str(self.user2) == 'dummy2', False)
        self.assertEqual(self.user3.username, 'dummy3')


class RoomTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='dummy topic', email='dummy@emai.com', password='321Qwerty')
        self.user2 = User.objects.create_user(username='participant', password='321Ytrewq')
        self.topic = Topic.objects.create(name='Topic testing')
        self.room = Room.objects.create(host=self.user1, topic=self.topic,
                                        name='test test test', description='Some cool description')

    def test_room_creating(self):
        self.assertEqual(str(self.room), 'test test test')
        self.assertEqual(str(self.room.host), 'Dummy Topic')
        self.room.participants.add(self.user2)
        self.assertEqual(self.room.participants.count(), 1)


class MessageTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='0', password='456Golek')
        self.topic = Topic.objects.create(name='msg test')
        self.room = Room.objects.create(host=self.user1, topic=self.topic, name='-#0-1 test msg', description='Some cool description')
        self.msg1 = Message.objects.create(user=self.user1, room=self.room, body='Who tf write this?')
        self.msg2 = Message.objects.create(user=self.user1, room=self.room, body=1234)
        self.msg3 = Message.objects.create(user=self.user1, room=self.room, body='0123456789012345678901234567890123456789012345678901234567890123456789')

    def test_messages(self):
        self.assertEqual(str(self.msg1.room.host), '0')
        self.assertEqual(self.msg2.room.message_set.count(), 3)
        self.assertEqual(len(str(self.msg3)), 50)
        self.assertEqual(len(self.msg3.body), 70)
        self.assertEqual(self.msg2.body, 1234)
