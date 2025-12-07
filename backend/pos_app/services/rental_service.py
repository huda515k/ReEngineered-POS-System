"""
Rental Service - Business logic for rental operations
"""
from datetime import date
from ..models import Rental, Customer


class RentalService:
    """Service class for handling rental operations"""
    
    @staticmethod
    def get_customer_rentals(customer_phone):
        """Get all rentals for a customer"""
        customer = Customer.objects.get(phone_number=customer_phone)
        return Rental.objects.filter(customer=customer).order_by('-rental_date')
    
    @staticmethod
    def get_active_rentals(customer_phone):
        """Get active (unreturned) rentals for a customer"""
        customer = Customer.objects.get(phone_number=customer_phone)
        return Rental.objects.filter(customer=customer, is_returned=False)
    
    @staticmethod
    def get_overdue_rentals(customer_phone=None):
        """Get overdue rentals, optionally filtered by customer"""
        query = Rental.objects.filter(
            is_returned=False,
            due_date__lt=date.today()
        )
        
        if customer_phone:
            customer = Customer.objects.get(phone_number=customer_phone)
            query = query.filter(customer=customer)
        
        return query.order_by('due_date')
    
    @staticmethod
    def check_customer_has_outstanding_returns(customer_phone):
        """Check if customer has outstanding (unreturned) rentals"""
        return RentalService.get_active_rentals(customer_phone).exists()
    
    @staticmethod
    def get_rental_by_id(rental_id):
        """Get rental by ID"""
        return Rental.objects.get(id=rental_id)

