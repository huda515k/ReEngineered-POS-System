from django.db import models
from django.core.validators import MinValueValidator
from .transaction import Transaction
from .item import Item
from .customer import Customer
from datetime import date, timedelta


class Rental(models.Model):
    """Rental model representing item rentals"""
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='rentals')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='rentals')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rentals')
    rental_date = models.DateField(default=date.today)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    days_overdue = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = 'rentals'
        ordering = ['-rental_date']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['item']),
            models.Index(fields=['is_returned']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        status = "Returned" if self.is_returned else "Active"
        return f"Rental #{self.id}: {self.item.name} - {self.customer.phone_number} ({status})"
    
    def save(self, *args, **kwargs):
        """Calculate due date and days overdue if not set"""
        if not self.due_date:
            # Default rental period: 7 days
            self.due_date = self.rental_date + timedelta(days=7)
        
        if not self.is_returned and self.due_date < date.today():
            self.days_overdue = (date.today() - self.due_date).days
        elif self.is_returned and self.return_date and self.return_date > self.due_date:
            self.days_overdue = (self.return_date - self.due_date).days
        else:
            self.days_overdue = None
        
        super().save(*args, **kwargs)
    
    def mark_as_returned(self, return_date=None):
        """Mark rental as returned"""
        self.is_returned = True
        self.return_date = return_date or date.today()
        self.save()
    
    def is_overdue(self):
        """Check if rental is overdue"""
        return not self.is_returned and self.due_date < date.today()

