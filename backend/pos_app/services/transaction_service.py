"""
Transaction Service - Business logic for transaction operations
"""
from decimal import Decimal
from django.db import transaction
from ..models import Transaction, TransactionItem, Item, Employee, Customer, Coupon
from ..models.audit_log import AuditLog


class TransactionService:
    """Service class for handling transaction business logic"""
    
    DEFAULT_TAX_RATE = Decimal('0.06')  # 6% tax
    DEFAULT_DISCOUNT = Decimal('0.90')  # 10% discount (0.90 multiplier)
    
    @staticmethod
    @transaction.atomic
    def create_sale(employee_id, items_data, coupon_code=None):
        """
        Create a sale transaction
        
        Args:
            employee_id: ID of the employee processing the sale
            items_data: List of dicts with 'item_id', 'quantity'
            coupon_code: Optional coupon code
        
        Returns:
            Transaction object
        """
        employee = Employee.objects.get(id=employee_id)
        total_amount = Decimal('0.00')
        transaction_items = []
        
        # Validate and prepare items
        for item_data in items_data:
            item = Item.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']
            
            if not item.is_available(quantity):
                raise ValueError(f"Insufficient quantity for item {item.name}")
            
            subtotal = item.price * quantity
            total_amount += subtotal
            
            transaction_items.append({
                'item': item,
                'quantity': quantity,
                'unit_price': item.price,
                'subtotal': subtotal
            })
        
        # Apply coupon discount if provided
        discount_applied = False
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    total_amount = Decimal(str(coupon.apply_discount(total_amount)))
                    discount_applied = True
            except Coupon.DoesNotExist:
                pass  # Invalid coupon, proceed without discount
        
        # Apply tax
        tax_rate = TransactionService.DEFAULT_TAX_RATE
        total_with_tax = total_amount * (1 + tax_rate)
        
        # Create transaction
        sale_transaction = Transaction.objects.create(
            transaction_type='Sale',
            employee=employee,
            total_amount=total_with_tax,
            tax_rate=tax_rate,
            discount_applied=discount_applied,
            coupon_code=coupon_code if discount_applied else None
        )
        
        # Create transaction items and update inventory
        for item_data in transaction_items:
            TransactionItem.objects.create(
                transaction=sale_transaction,
                item=item_data['item'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                subtotal=item_data['subtotal']
            )
            # Reduce inventory
            item_data['item'].reduce_quantity(item_data['quantity'])
        
        # Log transaction
        AuditLog.objects.create(
            employee=employee,
            action='transaction_created',
            details=f"Sale transaction #{sale_transaction.id} created"
        )
        
        return sale_transaction
    
    @staticmethod
    @transaction.atomic
    def create_rental(employee_id, customer_phone, items_data):
        """
        Create a rental transaction
        
        Args:
            employee_id: ID of the employee processing the rental
            customer_phone: Customer phone number
            items_data: List of dicts with 'item_id', 'quantity'
        
        Returns:
            Transaction object with associated rentals
        """
        from datetime import date, timedelta
        from ..models import Customer, Rental
        
        employee = Employee.objects.get(id=employee_id)
        
        # Get or create customer
        customer, created = Customer.objects.get_or_create(phone_number=customer_phone)
        
        total_amount = Decimal('0.00')
        transaction_items = []
        rentals_to_create = []
        
        # Validate and prepare items
        for item_data in items_data:
            item = Item.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']
            
            if not item.is_available(quantity):
                raise ValueError(f"Insufficient quantity for item {item.name}")
            
            subtotal = item.price * quantity
            total_amount += subtotal
            
            transaction_items.append({
                'item': item,
                'quantity': quantity,
                'unit_price': item.price,
                'subtotal': subtotal
            })
            
            # Prepare rental entries
            rental_date = date.today()
            due_date = rental_date + timedelta(days=7)  # 7-day rental period
            
            for _ in range(quantity):
                rentals_to_create.append({
                    'item': item,
                    'customer': customer,
                    'rental_date': rental_date,
                    'due_date': due_date
                })
        
        # Apply tax
        tax_rate = TransactionService.DEFAULT_TAX_RATE
        total_with_tax = total_amount * (1 + tax_rate)
        
        # Create transaction
        rental_transaction = Transaction.objects.create(
            transaction_type='Rental',
            employee=employee,
            customer=customer,
            total_amount=total_with_tax,
            tax_rate=tax_rate
        )
        
        # Create transaction items and rentals, update inventory
        for item_data in transaction_items:
            TransactionItem.objects.create(
                transaction=rental_transaction,
                item=item_data['item'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                subtotal=item_data['subtotal']
            )
            # Reduce inventory
            item_data['item'].reduce_quantity(item_data['quantity'])
        
        # Create rental records
        for rental_data in rentals_to_create:
            Rental.objects.create(
                transaction=rental_transaction,
                **rental_data
            )
        
        # Log transaction
        AuditLog.objects.create(
            employee=employee,
            action='transaction_created',
            details=f"Rental transaction #{rental_transaction.id} created for customer {customer_phone}"
        )
        
        return rental_transaction
    
    @staticmethod
    @transaction.atomic
    def process_return(customer_phone, item_ids):
        """
        Process item returns
        
        Args:
            customer_phone: Customer phone number
            item_ids: List of item IDs to return
        
        Returns:
            List of updated Rental objects
        """
        from datetime import date
        from ..models import Customer, Rental
        
        customer = Customer.objects.get(phone_number=customer_phone)
        returned_rentals = []
        
        # Find active rentals for these items
        active_rentals = Rental.objects.filter(
            customer=customer,
            item_id__in=item_ids,
            is_returned=False
        )
        
        if not active_rentals.exists():
            raise ValueError("No active rentals found for these items")
        
        return_date = date.today()
        
        for rental in active_rentals:
            rental.mark_as_returned(return_date)
            # Increase inventory
            rental.item.increase_quantity(1)
            returned_rentals.append(rental)
        
        return returned_rentals

