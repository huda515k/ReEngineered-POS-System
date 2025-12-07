from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..serializers import (
    TransactionSerializer, CreateSaleSerializer, CreateRentalSerializer
)
from ..services import TransactionService
from ..models import Transaction
from ..permissions import IsEmployeeAuthenticated


@api_view(['GET'])
@permission_classes([IsEmployeeAuthenticated])
def TransactionListView(request):
    """List all transactions"""
    transactions = Transaction.objects.all().order_by('-created_at')[:100]
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsEmployeeAuthenticated])
def TransactionDetailView(request, pk):
    """Retrieve a specific transaction"""
    try:
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    except Transaction.DoesNotExist:
        return Response(
            {'error': 'Transaction not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsEmployeeAuthenticated])
def CreateSaleView(request):
    """Create a new sale transaction"""
    employee_id = request.session.get('employee_id')
    
    if not employee_id:
        return Response(
            {'error': 'Employee not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    serializer = CreateSaleSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            transaction = TransactionService.create_sale(
                employee_id=employee_id,
                items_data=serializer.validated_data['items'],
                coupon_code=serializer.validated_data.get('coupon_code')
            )
            return Response(
                TransactionSerializer(transaction).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsEmployeeAuthenticated])
def CreateRentalView(request):
    """Create a new rental transaction"""
    employee_id = request.session.get('employee_id')
    
    if not employee_id:
        return Response(
            {'error': 'Employee not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    serializer = CreateRentalSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            transaction = TransactionService.create_rental(
                employee_id=employee_id,
                customer_phone=serializer.validated_data['customer_phone'],
                items_data=serializer.validated_data['items']
            )
            return Response(
                TransactionSerializer(transaction).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsEmployeeAuthenticated])
def GetOutstandingRentalsView(request):
    """Get outstanding (unreturned) rentals for a customer"""
    customer_phone = request.query_params.get('customer_phone')
    
    if not customer_phone:
        return Response(
            {'error': 'customer_phone parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from ..services import RentalService
        from ..serializers import RentalSerializer
        
        rentals = RentalService.get_active_rentals(customer_phone)
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsEmployeeAuthenticated])
def ProcessReturnView(request):
    """Process item returns"""
    customer_phone = request.data.get('customer_phone')
    item_ids = request.data.get('item_ids', [])
    
    if not customer_phone or not item_ids:
        return Response(
            {'error': 'customer_phone and item_ids are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        returned_rentals = TransactionService.process_return(customer_phone, item_ids)
        from ..serializers import RentalSerializer
        serializer = RentalSerializer(returned_rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

