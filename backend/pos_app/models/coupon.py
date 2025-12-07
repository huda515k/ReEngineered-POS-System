from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """Coupon model representing discount coupons"""
    
    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=10.0
    )
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coupons'
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Coupon: {self.code} ({self.discount_percentage}% off)"
    
    def is_valid(self):
        """Check if coupon is valid (active and not expired)"""
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
    
    def apply_discount(self, amount):
        """Apply discount to amount and return discounted value"""
        if not self.is_valid():
            return amount
        discount = float(amount) * (float(self.discount_percentage) / 100)
        return float(amount) - discount

