from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['user_id', 'created_at', 'updated_at']