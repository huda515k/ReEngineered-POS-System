from django.db import models
from .employee import Employee


class AuditLog(models.Model):
    """AuditLog model for tracking employee actions"""
    
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('transaction_created', 'Transaction Created'),
        ('transaction_updated', 'Transaction Updated'),
        ('employee_created', 'Employee Created'),
        ('employee_updated', 'Employee Updated'),
        ('employee_deleted', 'Employee Deleted'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.employee.username} - {self.action} at {self.timestamp}"

