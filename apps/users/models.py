import uuid
import bcrypt
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Partner', 'Partner'),
    ]
    
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
    
    def save(self, *args, **kwargs):
        # Hash password if it's being set/changed
        if self.pk is None or 'password' in kwargs.get('update_fields', []):
            if not self.password.startswith('$2b$'):  # Check if already hashed
                self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        super().save(*args, **kwargs)
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"