import jwt
from django.conf import settings
from django.http import JsonResponse
from apps.users.models import User

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication for certain paths
        skip_paths = ['/admin/', '/api/users/login/', '/api/users/signup/', '/', '/api/docs/', '/api/redoc/', '/api/schema/']
        
        if any(request.path.startswith(path) for path in skip_paths):
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Missing or invalid token'}, status=401)
        
        token = auth_header.split(' ')[1]
        
        try:
            decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            user = User.objects.get(user_id=decoded['user_id'])
            
            # Add user info to request
            request.user_data = {
                'id': str(user.user_id),
                'role': user.role,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}",
            }
            
        except (jwt.InvalidTokenError, User.DoesNotExist, KeyError):
            return JsonResponse({'error': 'Invalid or expired token'}, status=403)
        
        return self.get_response(request)