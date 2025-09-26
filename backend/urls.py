from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home_view(request):
    return JsonResponse({
        'message': 'Bintel ERP Backend is running',
        'version': '1.0.0',
        'documentation': {
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
            'schema': '/api/schema/'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/requests/', include('apps.requests.urls')),
]