from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'home.html', context)


def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all()
    room_participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room,
               'room_messages': room_messages,
               'room_participants': room_participants}
    return render(request, 'room.html', context)


def create_room(request):
    room_form = RoomForm
    page = 'create-room'
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(host=request.user,
                            topic=topic,
                            name=request.POST.get('name'),
                            description=request.POST.get('description')).participants.add(request.user)

        return redirect('home')

    context = {'room_form': room_form,
               'page': page,
               'topics': topics}
    return render(request, 'room_form.html', context)
