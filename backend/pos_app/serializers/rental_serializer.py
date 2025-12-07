from rest_framework import serializers
from ..models import Rental


class RentalSerializer(serializers.ModelSerializer):
    """Serializer for Rental model"""
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_id = serializers.IntegerField(source='item.id', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone_number', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Rental
        fields = [
            'id', 'transaction', 'item', 'item_id', 'item_name',
            'customer', 'customer_phone', 'rental_date', 'due_date',
            'return_date', 'is_returned', 'days_overdue', 'is_overdue'
        ]
        read_only_fields = ['id']
    
    def get_is_overdue(self, obj):
        """Check if rental is overdue"""
        return obj.is_overdue()

