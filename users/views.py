from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import timedelta
from .models import User, Profile, Star
from .serializers import (
    UserRegistrationSerializer, UserSerializer, ProfileSerializer, StarSerializer,
    AdminUserCreateSerializer, AdminUserUpdateSerializer
)
from rest_framework import viewsets

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    print(f"Login attempt: email={email}, password provided={bool(password)}")  # Debug logging

    if email and password:
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.email}, is_active={user.is_active}")  # Debug logging
            if user.check_password(password) and user.is_active:
                print("Password check passed, generating tokens")  # Debug logging
                login(request, user) # Create a session for browser users
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                print("Password check failed or user inactive")  # Debug logging
        except User.DoesNotExist:
            print(f"User with email {email} does not exist")  # Debug logging
    else:
        print("Email or password missing")  # Debug logging
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Check if user already has a profile
        if hasattr(self.request.user, 'profile'):
            # Update existing profile instead of creating new one
            profile = self.request.user.profile
            for attr, value in serializer.validated_data.items():
                setattr(profile, attr, value)
            profile.save()
        else:
            serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            if self.action == 'create':
                return AdminUserCreateSerializer
            elif self.action in ['update', 'partial_update']:
                return AdminUserUpdateSerializer
        
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

class StarListCreateView(generics.ListCreateAPIView):
    serializer_class = StarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Star.objects.all()

class StarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    permission_classes = [IsAuthenticated]

class UserStarsView(generics.ListAPIView):
    serializer_class = StarSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Star.objects.filter(receiver_id=user_id)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def give_star(request, user_id):
    if str(request.user.id) == str(user_id):
        return Response({'error': 'Cannot give star to yourself'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receiver = User.objects.get(id=user_id)
        star, created = Star.objects.get_or_create(giver=request.user, receiver=receiver)
        if created:
            return Response({
                'message': 'Star given successfully',
                'action': 'given',
                'total_stars': receiver.star_rating
            })
        else:
            star.delete()
            return Response({
                'message': 'Star removed',
                'action': 'removed',
                'total_stars': receiver.star_rating
            })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

def get_online_users():
    threshold = timezone.now() - timedelta(minutes=5)
    online_users = User.objects.filter(
        last_activity__gte=threshold
    )
    return online_users
