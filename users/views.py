from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Profile, Star
from .serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer, StarSerializer

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

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def give_star(request, user_id):
    try:
        receiver = User.objects.get(id=user_id)
        star, created = Star.objects.get_or_create(giver=request.user, receiver=receiver)
        if created:
            return Response({'message': 'Star given successfully'})
        else:
            star.delete()
            return Response({'message': 'Star removed'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)