from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

def home_view(request):
    html = '''
    <html>
    <body style="display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#000;font-family:Arial;">
        <h1 style="color:#fff;font-size:3rem;">Server is running</h1>
    </body>
    </html>
    '''
    return HttpResponse(html)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'auth': reverse('users:user-list', request=request, format=format),
        'events': reverse('events:event-list', request=request, format=format),
        'posts': reverse('posts:post-list', request=request, format=format),
        'notifications': reverse('notifications:notification-list', request=request, format=format),
        'swagger': reverse('schema-swagger-ui', request=request, format=format),
    })