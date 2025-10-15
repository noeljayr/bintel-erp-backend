import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiParameter
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    PasswordUpdateSerializer, PasswordResetSerializer, TokenResponseSerializer,
    MessageResponseSerializer, UserUpdateSerializer
)

@extend_schema(
    tags=['Users'],
    summary='Get all users',
    description='Retrieve a list of all users with optional role filtering',
    parameters=[
        OpenApiParameter(
            name='role',
            description='Filter users by role',
            required=False,
            type=str,
            enum=['Employee', 'Partner']
        ),
    ],
    responses={200: UserSerializer(many=True)},
    examples=[
        OpenApiExample(
            'Success Response',
            value=[
                {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "role": "Employee",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            ]
        )
    ]
)
@api_view(['GET'])
def get_users(request):
    role = request.query_params.get('role')
    
    if role:
        users = User.objects.filter(role=role)
    else:
        users = User.objects.all()
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@extend_schema(
    tags=['Authentication'],
    summary='User login',
    description='Authenticate user and return JWT token',
    request=LoginSerializer,
    responses={
        200: TokenResponseSerializer,
        400: MessageResponseSerializer,
        404: MessageResponseSerializer
    },
    examples=[
        OpenApiExample(
            'Login Request',
            value={
                "email": "user@example.com",
                "password": "password123"
            }
        )
    ]
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    payload = {
        'user_id': str(user.user_id),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return Response({'token': token})

@extend_schema(
    tags=['Authentication'],
    summary='User registration',
    description='Create a new user account',
    request=UserCreateSerializer,
    responses={
        200: MessageResponseSerializer,
        400: OpenApiResponse(description='Validation errors')
    },
    examples=[
        OpenApiExample(
            'Registration Request',
            value={
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "role": "Employee",
                "password": "securepassword123"
            }
        )
    ]
)
@api_view(['POST'])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    if User.objects.filter(email=serializer.validated_data['email']).exists():
        return Response({'message': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if phone already exists
    if User.objects.filter(phone=serializer.validated_data['phone']).exists():
        return Response({'message': 'Phone already taken'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = serializer.save()
    return Response({'message': "You're all set."})

@extend_schema(
    tags=['Users'],
    summary='Update user profile',
    description='Update user information (requires authentication)',
    request=UserUpdateSerializer,
    responses={
        200: OpenApiResponse(description='User updated successfully with new token'),
        401: MessageResponseSerializer
    }
)
@api_view(['PUT'])
def edit_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({'message': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        user_id = decoded['user_id']
    except (jwt.InvalidTokenError, IndexError, KeyError):
        return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Update user information
    if 'first_name' in request.data:
        user.first_name = request.data['first_name']
    if 'last_name' in request.data:
        user.last_name = request.data['last_name']
    if 'email' in request.data:
        user.email = request.data['email']
    
    user.save()
    
    # Generate new token
    payload = {
        'user_id': str(user.user_id),
        'full_name': f"{user.first_name} {user.last_name}",
        'email': user.email,
    }
    
    new_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return Response({
        'message': 'Update successfully',
        'token': new_token
    })

@extend_schema(
    tags=['Users'],
    summary='Update password',
    description='Change user password (requires authentication)',
    request=PasswordUpdateSerializer,
    responses={
        200: MessageResponseSerializer,
        400: MessageResponseSerializer,
        401: MessageResponseSerializer
    }
)
@api_view(['PUT'])
def update_password(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({'message': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        user_id = decoded['user_id']
    except (jwt.InvalidTokenError, IndexError, KeyError):
        return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = PasswordUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    current_password = serializer.validated_data['currentPassword']
    new_password = serializer.validated_data['newPassword']
    
    if not user.check_password(current_password):
        return Response({'message': 'Incorrect current password.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.password = new_password
    user.save()
    
    return Response({'message': 'Password updated successfully.'})

@extend_schema(
    tags=['Users'],
    summary='Reset password',
    description='Reset user password by email',
    request=PasswordResetSerializer,
    responses={
        200: MessageResponseSerializer,
        404: MessageResponseSerializer
    }
)
@api_view(['POST'])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    new_password = serializer.validated_data['new_password']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user.password = new_password
    user.save()
    
    return Response({'message': 'Password reset successfully'})

@extend_schema(
    tags=['Users'],
    summary='Delete user account',
    description='Delete user account. Users can delete their own account, Partners can delete any user account. Note: This action is irreversible and will also delete all associated requests.',
    responses={
        200: MessageResponseSerializer,
        401: MessageResponseSerializer,
        403: MessageResponseSerializer,
        404: MessageResponseSerializer,
        409: MessageResponseSerializer
    },
    examples=[
        OpenApiExample(
            'Success Response',
            value={"message": "User account deleted successfully"}
        )
    ]
)
@api_view(['DELETE'])
def delete_user(request, user_id=None):
    # Get authentication token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({'message': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        current_user_id = decoded['user_id']
        current_user_role = decoded.get('role', 'Employee')
    except (jwt.InvalidTokenError, IndexError, KeyError):
        return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Determine which user to delete
    target_user_id = user_id if user_id else current_user_id
    
    # Get current user for authorization checks
    try:
        current_user = User.objects.get(user_id=current_user_id)
    except User.DoesNotExist:
        return Response({'message': 'Current user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get target user to delete
    try:
        target_user = User.objects.get(user_id=target_user_id)
    except User.DoesNotExist:
        return Response({'message': 'User to delete not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Authorization checks
    if target_user_id != current_user_id:
        # Trying to delete another user - only Partners can do this
        if current_user.role != 'Partner':
            return Response({
                'message': 'Only Partners can delete other user accounts'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Prevent Partners from deleting other Partners (optional safety measure)
        if target_user.role == 'Partner' and current_user.role == 'Partner':
            return Response({
                'message': 'Partners cannot delete other Partner accounts'
            }, status=status.HTTP_403_FORBIDDEN)
    
    # Check and handle associated requests
    from apps.requests.models import Request
    user_requests = Request.objects.filter(request_by=target_user_id)
    request_count = user_requests.count()
    
    # Also check for requests where this user is the approver
    approver_requests = Request.objects.filter(approver_id=target_user_id, status='Pending')
    approver_count = approver_requests.count()
    
    # Store user info for response
    deleted_user_name = f"{target_user.first_name} {target_user.last_name}"
    deleted_user_email = target_user.email
    
    # Delete associated requests first (since there's no proper FK cascade)
    if request_count > 0:
        user_requests.delete()
    
    # Handle requests where this user was the approver (set to null or reassign)
    if approver_count > 0:
        # For now, we'll leave these requests as orphaned (you might want to reassign them)
        # In a production system, you'd want to reassign to another Partner
        pass
    
    # Delete the user
    target_user.delete()
    
    # Prepare response message
    base_message = f'User account for {deleted_user_name} ({deleted_user_email}) has been deleted successfully'
    if target_user_id == current_user_id:
        base_message = 'Your account has been deleted successfully'
    
    # Add information about deleted requests if any existed
    if request_count > 0:
        base_message += f' along with {request_count} associated request(s)'
    
    if approver_count > 0:
        base_message += f' (Note: {approver_count} pending request(s) were left without an approver)'
    
    return Response({'message': base_message})