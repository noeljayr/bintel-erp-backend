import uuid
import random
from django.db import models
from apps.users.models import User

class Request(models.Model):
    CURRENCY_CHOICES = [
        ('MWK', 'MWK'),
        ('USD', 'USD'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_id = models.UUIDField(default=uuid.uuid4, editable=False)
    request_number = models.IntegerField(unique=True)
    request_by = models.UUIDField()  # References User.user_id
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    approver_id = models.UUIDField()  # References User.user_id
    purpose = models.TextField()
    description = models.TextField(blank=True, null=True)
    initiated_on = models.DateTimeField(auto_now_add=True)
    required_on = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'requests'
        ordering = ['-updated_at']
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = self.generate_unique_request_number()
        super().save(*args, **kwargs)
    
    def generate_unique_request_number(self):
        """Generate a unique request number between 10000-99999"""
        for _ in range(10):  # Try up to 10 times
            number = random.randint(10000, 99999)
            if not Request.objects.filter(request_number=number).exists():
                return number
        raise ValueError("Failed to generate a unique request number after multiple attempts.")
    
    def __str__(self):
        return f"Request #{self.request_number} - {self.purpose[:50]}"