from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from accounts.views import home
import mimetypes

# Ensure all video MIME types are registered
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('video/webm', '.webm')
mimetypes.add_type('video/ogg', '.ogv')
mimetypes.add_type('video/quicktime', '.mov')

# Custom serve function to handle MIME types correctly
def media_serve(request, path, document_root=None):
    response = serve(request, path, document_root)
    
    # Check if file is a video and set the correct MIME type
    if path.lower().endswith(('.mp4', '.webm', '.ogv', '.mov')):
        ext = path.split('.')[-1].lower()
        content_type = {
            'mp4': 'video/mp4',
            'webm': 'video/webm',
            'ogv': 'video/ogg',
            'mov': 'video/quicktime'
        }.get(ext, 'application/octet-stream')
        
        response['Content-Type'] = content_type
    
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('forums/', include('forums.urls', namespace='forums')),
    path('courses/', include('courses.urls', namespace='courses')),  # Add this line
    path('projects/', include('projects.urls', namespace='projects')),
    path('events/', include('events.urls')),
]

# Always include media files URL pattern regardless of DEBUG setting
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', media_serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# Still add the normal static urls for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)