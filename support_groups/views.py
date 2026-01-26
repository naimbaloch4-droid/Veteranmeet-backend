from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import SupportGroup, GroupMembership, GroupPost
from .serializers import SupportGroupSerializer, GroupMembershipSerializer, GroupPostSerializer

class SupportGroupViewSet(viewsets.ModelViewSet):
    serializer_class = SupportGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SupportGroup.objects.all()
        queryset = SupportGroup.objects.all()
        topic = self.request.query_params.get('topic')
        if topic:
            queryset = queryset.filter(topic__icontains=topic)
        return queryset.filter(privacy_level='public').union(
            queryset.filter(members=self.request.user)
        ).distinct()

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        group = self.get_object()
        membership, created = GroupMembership.objects.get_or_create(
            user=request.user,
            group=group,
            defaults={'role': 'member'}
        )
        if created:
            return Response({'status': 'joined group'})
        return Response({'status': 'already a member'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        group = self.get_object()
        try:
            membership = GroupMembership.objects.get(user=request.user, group=group)
            membership.delete()
            return Response({'status': 'left group'})
        except GroupMembership.DoesNotExist:
            return Response({'error': 'not a member'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        group = self.get_object()
        memberships = GroupMembership.objects.filter(group=group)
        serializer = GroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def posts(self, request, pk=None):
        group = self.get_object()
        
        # Check if user is member (Superusers bypass)
        if not self.request.user.is_superuser and not group.members.filter(id=request.user.id).exists():
            return Response({'error': 'must be member to view posts'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'GET':
            posts = GroupPost.objects.filter(group=group)
            serializer = GroupPostSerializer(posts, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = GroupPostSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(group=group)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupPostViewSet(viewsets.ModelViewSet):
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return GroupPost.objects.all()
        return GroupPost.objects.filter(group__members=self.request.user)