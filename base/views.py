from django.shortcuts import render
from .models import Room, Topic, Message, User

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'home.html', context)