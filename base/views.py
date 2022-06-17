from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, MyUserCreationForm, UserForm
from .models import Room, Topic, Message, User
from django.contrib import messages
from django.db.models import Q


def home(request):
    rooms_count = Room.objects.count()
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(name__icontains=query) |
                                Q(topic__name__icontains=query) |
                                Q(description__icontains=query) |
                                Q(host__username__icontains=query))

    rooms_messages = Message.objects.filter(Q(room__topic__name__icontains=query) |
                                            Q(room__name__icontains=query) |
                                            Q(room__host__username__icontains=query))

    context = {'rooms': rooms,
               'topics': topics,
               'rooms_count': rooms_count,
               'rooms_messages': rooms_messages}
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


@login_required(login_url='login_user')
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


@login_required(login_url='login_user')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    room_form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk)

    context = {'room': room,
               'room_form': room_form,
               'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url='login_user')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room': room}
    return render(request, 'delete.html', context)


def register_user(request):
    page = 'register'
    form = MyUserCreationForm

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {'page': page,
               'form': form}
    return render(request, 'login-register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login-register.html')


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('home')
