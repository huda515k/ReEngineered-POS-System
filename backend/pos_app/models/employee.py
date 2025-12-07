from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Employee(models.Model):
    """Employee model representing system users (Admin/Cashier)"""
    
    POSITION_CHOICES = [
        ('Admin', 'Admin'),
        ('Cashier', 'Cashier'),
    ]
    
    username = models.CharField(max_length=50, unique=True, db_index=True)
    password_hash = models.CharField(max_length=255)  # Store hashed password
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['username']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['position']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.position})"
    
    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches"""
        return check_password(raw_password, self.password_hash)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def is_admin(self):
        return self.position == 'Admin'
    
    def is_cashier(self):
        return self.position == 'Cashier'

