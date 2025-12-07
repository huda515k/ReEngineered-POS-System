from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    """Item model representing inventory items"""
    
    legacy_item_id = models.IntegerField(unique=True, db_index=True, help_text="Original item ID from legacy system")
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'items'
        ordering = ['legacy_item_id']
        indexes = [
            models.Index(fields=['legacy_item_id']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.legacy_item_id} - {self.name} (${self.price})"
    
    def is_available(self, requested_quantity=1):
        """Check if item is available in requested quantity"""
        return self.quantity >= requested_quantity
    
    def reduce_quantity(self, amount):
        """Reduce item quantity by specified amount"""
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        return False
    
    def increase_quantity(self, amount):
        """Increase item quantity by specified amount"""
        self.quantity += amount
        self.save()
        return True

