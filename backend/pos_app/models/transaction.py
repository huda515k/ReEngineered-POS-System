from django.db import models
from django.core.validators import MinValueValidator
from .employee import Employee
from .customer import Customer


class Transaction(models.Model):
    """Transaction model representing sales, rentals, and returns"""
    
    TRANSACTION_TYPES = [
        ('Sale', 'Sale'),
        ('Rental', 'Rental'),
        ('Return', 'Return'),
    ]
    
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='transactions')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.06)  # Default 6% tax
    discount_applied = models.BooleanField(default=False)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_type']),
            models.Index(fields=['employee']),
            models.Index(fields=['customer']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} #{self.id} - ${self.total_amount} ({self.created_at})"
    
    def calculate_total_with_tax(self):
        """Calculate total with tax"""
        return float(self.total_amount) * (1 + float(self.tax_rate))


class TransactionItem(models.Model):
    """TransactionItem model representing items in a transaction"""
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='transaction_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        db_table = 'transaction_items'
        indexes = [
            models.Index(fields=['transaction']),
            models.Index(fields=['item']),
        ]
    
    def __str__(self):
        return f"{self.item.name} x{self.quantity} = ${self.subtotal}"
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving"""
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

