from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Request
from apps.users.models import User
from apps.users.serializers import UserSerializer

class RequestSerializer(serializers.ModelSerializer):
    approver = serializers.SerializerMethodField()
    requested_by = serializers.SerializerMethodField()
    
    class Meta:
        model = Request
        fields = [
            'id', 'request_id', 'request_number', 'request_by', 'amount', 
            'currency', 'approver_id', 'purpose', 'description', 
            'initiated_on', 'required_on', 'status', 'created_at', 
            'updated_at', 'approver', 'requested_by'
        ]
        read_only_fields = ['id', 'request_id', 'request_number', 'created_at', 'updated_at']
    
    @extend_schema_field(UserSerializer)
    def get_approver(self, obj):
        try:
            user = User.objects.get(user_id=obj.approver_id)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None
    
    @extend_schema_field(UserSerializer)
    def get_requested_by(self, obj):
        try:
            user = User.objects.get(user_id=obj.request_by)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None

class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = [
            'amount', 'currency', 'approver_id', 'purpose', 
            'description', 'required_on'
        ]

class RequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['status']

class RequestEditSerializer(serializers.ModelSerializer):
    """Serializer for editing request details (pending requests only)"""
    class Meta:
        model = Request
        fields = [
            'amount', 'currency', 'approver_id', 'purpose', 
            'description', 'required_on'
        ]

class RequestListResponseSerializer(serializers.Serializer):
    page = serializers.IntegerField(help_text="Current page number")
    limit = serializers.IntegerField(help_text="Items per page")
    total = serializers.IntegerField(help_text="Total number of requests")
    totalPages = serializers.IntegerField(help_text="Total number of pages")
    statusCounts = serializers.DictField(help_text="Count of requests by status")
    data = RequestSerializer(many=True, help_text="List of requests")