"""
Inventory Service - Business logic for inventory operations
"""
from ..models import Item


class InventoryService:
    """Service class for handling inventory operations"""
    
    @staticmethod
    def get_all_items():
        """Get all items in inventory"""
        return Item.objects.all().order_by('legacy_item_id')
    
    @staticmethod
    def get_item_by_id(item_id):
        """Get item by ID"""
        return Item.objects.get(id=item_id)
    
    @staticmethod
    def get_item_by_legacy_id(legacy_item_id):
        """Get item by legacy item ID"""
        return Item.objects.get(legacy_item_id=legacy_item_id)
    
    @staticmethod
    def search_items(query):
        """Search items by name or legacy ID"""
        return Item.objects.filter(
            name__icontains=query
        ) | Item.objects.filter(
            legacy_item_id__icontains=query
        )
    
    @staticmethod
    def update_item_quantity(item_id, new_quantity):
        """Update item quantity"""
        item = Item.objects.get(id=item_id)
        item.quantity = new_quantity
        item.save()
        return item
    
    @staticmethod
    def check_availability(item_id, requested_quantity):
        """Check if item is available in requested quantity"""
        item = Item.objects.get(id=item_id)
        return item.is_available(requested_quantity)

