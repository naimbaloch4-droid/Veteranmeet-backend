from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Follow

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user == request.user:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    
    if created:
        return Response({'message': 'Successfully followed user'})
    else:
        follow.delete()
        return Response({'message': 'Unfollowed user'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # Get posts from followed users
    following_users = request.user.following.values_list('following', flat=True)
    from posts.models import Post
    from posts.serializers import PostSerializer
    
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')[:20]
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    followers = User.objects.filter(following__following=request.user)
    from .serializers import UserSerializer
    serializer = UserSerializer(followers, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    following = User.objects.filter(followers__follower=request.user)
    from .serializers import UserSerializer
    serializer = UserSerializer(following, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggestions(request):
    # Suggest users that the current user is not already following
    following_ids = request.user.following.values_list('following_id', flat=True)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=request.user.id).order_by('?')[:5]
    
    from .serializers import UserSerializer
    serializer = UserSerializer(suggestions, many=True, context={'request': request})
    return Response(serializer.data)