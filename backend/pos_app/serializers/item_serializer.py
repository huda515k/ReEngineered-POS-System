from rest_framework import serializers
from ..models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model"""
    
    class Meta:
        model = Item
        fields = ['id', 'legacy_item_id', 'name', 'price', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

