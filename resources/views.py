from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ResourceCategory, Resource, ResourceRating, ResourceBookmark
from .serializers import ResourceCategorySerializer, ResourceSerializer, ResourceRatingSerializer, ResourceBookmarkSerializer

class ResourceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResourceCategory.objects.all()
    serializer_class = ResourceCategorySerializer
    permission_classes = [IsAuthenticated]

class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Resource.objects.all()
        category = self.request.query_params.get('category')
        location = self.request.query_params.get('location')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        resource = self.get_object()
        bookmark, created = ResourceBookmark.objects.get_or_create(
            user=request.user,
            resource=resource
        )
        if created:
            return Response({'status': 'bookmarked'})
        else:
            bookmark.delete()
            return Response({'status': 'bookmark removed'})

    @action(detail=True, methods=['get', 'post'])
    def ratings(self, request, pk=None):
        resource = self.get_object()
        
        if request.method == 'GET':
            ratings = ResourceRating.objects.filter(resource=resource)
            serializer = ResourceRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = ResourceRatingSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(resource=resource)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def bookmarked(self, request):
        bookmarks = ResourceBookmark.objects.filter(user=request.user)
        serializer = ResourceBookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)