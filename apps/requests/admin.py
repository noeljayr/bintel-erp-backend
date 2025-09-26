from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'purpose', 'amount', 'currency', 'status', 'initiated_on']
    list_filter = ['status', 'currency', 'initiated_on']
    search_fields = ['purpose', 'request_number']
    readonly_fields = ['id', 'request_id', 'request_number', 'created_at', 'updated_at']