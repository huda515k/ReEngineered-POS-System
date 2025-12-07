from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..serializers import ItemSerializer
from ..services import InventoryService
from ..permissions import IsEmployeeAuthenticated


@api_view(['GET'])
@permission_classes([IsEmployeeAuthenticated])
def ItemListView(request):
    """List all items or search items"""
    query = request.query_params.get('search', None)
    
    if query:
        items = InventoryService.search_items(query)
    else:
        items = InventoryService.get_all_items()
    
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsEmployeeAuthenticated])
def ItemDetailView(request, pk):
    """Retrieve a specific item"""
    try:
        item = InventoryService.get_item_by_id(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_404_NOT_FOUND
        )

