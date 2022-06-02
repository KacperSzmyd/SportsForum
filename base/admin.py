from django.contrib import admin
from .models import User, Message, Room, Topic

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
