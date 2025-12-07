from rest_framework import serializers
from ..models import Transaction, TransactionItem


class TransactionItemSerializer(serializers.ModelSerializer):
    """Serializer for TransactionItem model"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_id = serializers.IntegerField(source='item.id', read_only=True)
    
    class Meta:
        model = TransactionItem
        fields = ['id', 'item_id', 'item_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    items = TransactionItemSerializer(many=True, read_only=True)
    employee_username = serializers.CharField(source='employee.username', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone_number', read_only=True, allow_null=True)
    total_with_tax = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'employee', 'employee_username',
            'customer', 'customer_phone', 'total_amount', 'tax_rate',
            'total_with_tax', 'discount_applied', 'coupon_code',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_with_tax(self, obj):
        """Calculate total with tax"""
        return float(obj.total_amount) * (1 + float(obj.tax_rate))


class CreateSaleSerializer(serializers.Serializer):
    """Serializer for creating sale transactions"""
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        min_length=1
    )
    coupon_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def validate_items(self, value):
        """Validate items list"""
        for item in value:
            if 'item_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have 'item_id' and 'quantity'")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
        return value


class CreateRentalSerializer(serializers.Serializer):
    """Serializer for creating rental transactions"""
    customer_phone = serializers.CharField(max_length=15)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        min_length=1
    )
    
    def validate_items(self, value):
        """Validate items list"""
        for item in value:
            if 'item_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have 'item_id' and 'quantity'")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
        return value

