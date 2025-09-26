from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone', 'role', 'created_at', 'updated_at']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PasswordUpdateSerializer(serializers.Serializer):
    currentPassword = serializers.CharField()
    newPassword = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()

class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="JWT authentication token")

class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Response message")

class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, help_text="User's first name")
    last_name = serializers.CharField(required=False, help_text="User's last name") 
    email = serializers.EmailField(required=False, help_text="User's email address")