from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .views import ChatRoomViewSet, ChatMessageViewSet, heartbeat
from users.views import get_online_users
from users.serializers import UserSerializer

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='chatroom')
router.register(r'messages', ChatMessageViewSet, basename='chatmessage')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def online_users_view(request):
    """
    Returns a list of currently online user IDs.
    Users are considered online if their last_activity was within the last 5 minutes.
    """
    online_users = get_online_users()
    # Return just the user IDs as expected by the frontend
    online_user_ids = list(online_users.values_list('id', flat=True))
    return Response({'online_users': online_user_ids})

urlpatterns = [
    path('online-users/', online_users_view, name='online-users'),
    path('heartbeat/', heartbeat, name='heartbeat'),
    path('', include(router.urls)),
]