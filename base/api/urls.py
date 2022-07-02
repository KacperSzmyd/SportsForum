from django.urls import path, include
from rest_framework import routers

from base.api.views import RoomViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
