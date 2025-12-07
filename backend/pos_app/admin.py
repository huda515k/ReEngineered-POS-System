from django.contrib import admin
from .models import (
    Employee, Item, Customer, Transaction, TransactionItem,
    Rental, Coupon, AuditLog
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'position', 'is_active', 'created_at']
    list_filter = ['position', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['legacy_item_id', 'name', 'price', 'quantity', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'legacy_item_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'created_at']
    search_fields = ['phone_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_type', 'employee', 'customer', 'total_amount', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['employee__username', 'customer__phone_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'item', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['transaction__transaction_type']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'item', 'rental_date', 'due_date', 'is_returned', 'days_overdue']
    list_filter = ['is_returned', 'rental_date']
    search_fields = ['customer__phone_number', 'item__name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'is_active', 'expires_at', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['employee', 'action', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['employee__username']
    readonly_fields = ['timestamp']

