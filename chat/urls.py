from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .views import ChatRoomViewSet, ChatMessageViewSet
from users.views import get_online_users
from users.serializers import UserSerializer

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='chatroom')
router.register(r'messages', ChatMessageViewSet, basename='chatmessage')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def online_users_view(request):
    online_users = get_online_users()
    serializer = UserSerializer(online_users, many=True)
    return Response(serializer.data)

urlpatterns = [
    path('online-users/', online_users_view, name='online-users'),
    path('', include(router.urls)),
]