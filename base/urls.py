

from django.urls import path
from .views import home, room, create_room, update_room, delete_room, register_user, login_user, logout_user, delete_message, user_profile, update_user

urlpatterns = [
    path('', home, name='home'),
    path('room/<str:pk>/', room, name='room'),

    path('create-room/', create_room, name='create-room'),
    path('update-room/<str:pk>/', update_room, name='update-room'),
    path('delete-room/<str:pk>', delete_room, name='delete-room'),

    path('register/', register_user, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),

    path('delete-message/<str:pk>/', delete_message, name='delete-message'),

    path('user-progile/<str:pk>', user_profile, name='user-profile'),
    path('update-profile/<str:pk>/', update_user, name='update-user')
]