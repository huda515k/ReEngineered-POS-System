"""
Test Data Seeding Script
Generates test data for development and testing
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta
import random

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos_app.models import Employee, Item, Customer, Transaction, TransactionItem, Rental, Coupon
from pos_app.services import EmployeeService


def seed_employees(count=5):
    """Generate test employees"""
    print(f"Generating {count} test employees...")
    
    first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    positions = ['Admin', 'Cashier']
    
    created = 0
    for i in range(count):
        username = f"testuser{i+1}"
        if Employee.objects.filter(username=username).exists():
            continue
        
        try:
            EmployeeService.create_employee(
                username=username,
                password='testpass123',
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                position=random.choice(positions)
            )
            created += 1
        except Exception as e:
            print(f"  Error creating employee {username}: {e}")
    
    print(f"  ✅ Created {created} test employees")
    return created


def seed_items(count=20):
    """Generate test items"""
    print(f"Generating {count} test items...")
    
    item_names = [
        'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones',
        'Tablet', 'Phone', 'Charger', 'Cable', 'Adapter',
        'Speaker', 'Webcam', 'Microphone', 'Printer', 'Scanner',
        'Router', 'Switch', 'Hub', 'Modem', 'Access Point'
    ]
    
    created = 0
    for i in range(count):
        legacy_id = 2000 + i
        if Item.objects.filter(legacy_item_id=legacy_id).exists():
            continue
        
        try:
            Item.objects.create(
                legacy_item_id=legacy_id,
                name=random.choice(item_names) + f" {i+1}",
                price=Decimal(str(round(random.uniform(10.00, 500.00), 2))),
                quantity=random.randint(0, 100)
            )
            created += 1
        except Exception as e:
            print(f"  Error creating item {legacy_id}: {e}")
    
    print(f"  ✅ Created {created} test items")
    return created


def seed_customers(count=10):
    """Generate test customers"""
    print(f"Generating {count} test customers...")
    
    created = 0
    for i in range(count):
        # Generate random phone number
        phone = f"555{random.randint(1000000, 9999999)}"
        
        if Customer.objects.filter(phone_number=phone).exists():
            continue
        
        try:
            Customer.objects.create(phone_number=phone)
            created += 1
        except Exception as e:
            print(f"  Error creating customer {phone}: {e}")
    
    print(f"  ✅ Created {created} test customers")
    return created


def seed_transactions(count=15):
    """Generate test transactions"""
    print(f"Generating {count} test transactions...")
    
    employees = list(Employee.objects.all())
    customers = list(Customer.objects.all())
    items = list(Item.objects.all())
    transaction_types = ['Sale', 'Rental', 'Return']
    
    if not employees or not items:
        print("  ⚠️  Need employees and items to create transactions")
        return 0
    
    created = 0
    for i in range(count):
        try:
            employee = random.choice(employees)
            transaction_type = random.choice(transaction_types)
            
            # Select customer (optional for sales)
            customer = None
            if transaction_type in ['Rental', 'Return'] and customers:
                customer = random.choice(customers)
            elif customers and random.choice([True, False]):
                customer = random.choice(customers)
            
            # Create transaction
            transaction = Transaction.objects.create(
                transaction_type=transaction_type,
                employee=employee,
                customer=customer,
                total_amount=Decimal('0.00'),
                tax_rate=Decimal('0.06')
            )
            
            # Add items to transaction
            num_items = random.randint(1, 5)
            selected_items = random.sample(items, min(num_items, len(items)))
            
            total = Decimal('0.00')
            for item in selected_items:
                quantity = random.randint(1, 3)
                unit_price = item.price
                subtotal = unit_price * quantity
                total += subtotal
                
                TransactionItem.objects.create(
                    transaction=transaction,
                    item=item,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
            
            # Update transaction total
            tax_amount = total * transaction.tax_rate
            transaction.total_amount = total + tax_amount
            transaction.save()
            
            created += 1
        except Exception as e:
            print(f"  Error creating transaction: {e}")
    
    print(f"  ✅ Created {created} test transactions")
    return created


def seed_rentals(count=10):
    """Generate test rentals"""
    print(f"Generating {count} test rentals...")
    
    transactions = Transaction.objects.filter(transaction_type='Rental')
    items = list(Item.objects.all())
    customers = list(Customer.objects.all())
    
    if not transactions.exists() or not items or not customers:
        print("  ⚠️  Need rental transactions, items, and customers to create rentals")
        return 0
    
    created = 0
    for transaction in transactions[:count]:
        try:
            customer = transaction.customer or random.choice(customers)
            item = random.choice(items)
            
            rental_date = date.today() - timedelta(days=random.randint(0, 30))
            due_date = rental_date + timedelta(days=7)
            
            # Randomly mark some as returned
            is_returned = random.choice([True, False])
            return_date = rental_date + timedelta(days=random.randint(1, 14)) if is_returned else None
            
            Rental.objects.create(
                transaction=transaction,
                item=item,
                customer=customer,
                rental_date=rental_date,
                due_date=due_date,
                return_date=return_date,
                is_returned=is_returned
            )
            created += 1
        except Exception as e:
            print(f"  Error creating rental: {e}")
    
    print(f"  ✅ Created {created} test rentals")
    return created


def seed_coupons(count=5):
    """Generate test coupons"""
    print(f"Generating {count} test coupons...")
    
    created = 0
    for i in range(count):
        code = f"TEST{i+1}"
        if Coupon.objects.filter(code=code).exists():
            continue
        
        try:
            Coupon.objects.create(
                code=code,
                discount_percentage=Decimal(str(random.choice([5, 10, 15, 20]))),
                is_active=True
            )
            created += 1
        except Exception as e:
            print(f"  Error creating coupon {code}: {e}")
    
    print(f"  ✅ Created {created} test coupons")
    return created


def main():
    """Main seeding function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed test data for development')
    parser.add_argument('--employees', type=int, default=5, help='Number of employees to create')
    parser.add_argument('--items', type=int, default=20, help='Number of items to create')
    parser.add_argument('--customers', type=int, default=10, help='Number of customers to create')
    parser.add_argument('--transactions', type=int, default=15, help='Number of transactions to create')
    parser.add_argument('--rentals', type=int, default=10, help='Number of rentals to create')
    parser.add_argument('--coupons', type=int, default=5, help='Number of coupons to create')
    parser.add_argument('--all', action='store_true', help='Seed all data types')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Test Data Seeding Script")
    print("=" * 60)
    print()
    
    if args.all:
        seed_employees(args.employees)
        seed_items(args.items)
        seed_customers(args.customers)
        seed_transactions(args.transactions)
        seed_rentals(args.rentals)
        seed_coupons(args.coupons)
    else:
        if args.employees > 0:
            seed_employees(args.employees)
        if args.items > 0:
            seed_items(args.items)
        if args.customers > 0:
            seed_customers(args.customers)
        if args.transactions > 0:
            seed_transactions(args.transactions)
        if args.rentals > 0:
            seed_rentals(args.rentals)
        if args.coupons > 0:
            seed_coupons(args.coupons)
    
    print("\n" + "=" * 60)
    print("Seeding Complete!")
    print("=" * 60)
    print(f"Total Employees: {Employee.objects.count()}")
    print(f"Total Items: {Item.objects.count()}")
    print(f"Total Customers: {Customer.objects.count()}")
    print(f"Total Transactions: {Transaction.objects.count()}")
    print(f"Total Rentals: {Rental.objects.count()}")
    print(f"Total Coupons: {Coupon.objects.count()}")


if __name__ == '__main__':
    main()

