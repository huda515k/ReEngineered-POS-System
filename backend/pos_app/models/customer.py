from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    """Customer model representing rental customers"""
    
    phone_regex = RegexValidator(
        regex=r'^\d{10,15}$',
        message="Phone number must be 10-15 digits"
    )
    
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_regex],
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
        ordering = ['phone_number']
        indexes = [
            models.Index(fields=['phone_number']),
        ]
    
    def __str__(self):
        return f"Customer: {self.phone_number}"

