"""
Data Migration Script
Migrates data from legacy text files to PostgreSQL database
"""
import os
import sys
import django
from datetime import datetime
from decimal import Decimal

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos_app.models import Employee, Item, Customer, Rental, Coupon, Transaction, TransactionItem
from pos_app.services import EmployeeService


def migrate_employees(legacy_path):
    """Migrate employees from employeeDatabase.txt"""
    print("Migrating employees...")
    
    with open(legacy_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 5:
                continue
            
            username = parts[0]
            position = parts[1]
            first_name = parts[2]
            last_name = parts[3]
            password = parts[4]
            
            # Skip if employee already exists
            if Employee.objects.filter(username=username).exists():
                print(f"  Skipping existing employee: {username}")
                continue
            
            try:
                EmployeeService.create_employee(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    position=position
                )
                print(f"  Migrated employee: {username}")
            except Exception as e:
                print(f"  Error migrating employee {username}: {e}")
    
    print(f"Employee migration complete. Total: {Employee.objects.count()}")


def migrate_items(legacy_path):
    """Migrate items from itemDatabase.txt"""
    print("Migrating items...")
    
    with open(legacy_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 4:
                continue
            
            try:
                legacy_item_id = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                quantity = int(parts[3])
                
                # Skip if item already exists
                if Item.objects.filter(legacy_item_id=legacy_item_id).exists():
                    print(f"  Skipping existing item: {legacy_item_id}")
                    continue
                
                Item.objects.create(
                    legacy_item_id=legacy_item_id,
                    name=name,
                    price=Decimal(str(price)),
                    quantity=quantity
                )
                print(f"  Migrated item: {legacy_item_id} - {name}")
            except Exception as e:
                print(f"  Error migrating item: {e}")
    
    print(f"Item migration complete. Total: {Item.objects.count()}")


def migrate_customers_and_rentals(legacy_path):
    """Migrate customers and rentals from userDatabase.txt"""
    print("Migrating customers and rentals...")
    
    from datetime import datetime, timedelta
    
    with open(legacy_path, 'r') as f:
        # Skip header line
        next(f, None)
        
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 1:
                continue
            
            phone_number = parts[0]
            
            # Get or create customer
            customer, created = Customer.objects.get_or_create(phone_number=phone_number)
            if created:
                print(f"  Created customer: {phone_number}")
            
            # Parse rental entries (format: itemID,date,returned)
            if len(parts) > 1:
                for rental_entry in parts[1:]:
                    try:
                        rental_parts = rental_entry.split(',')
                        if len(rental_parts) < 3:
                            continue
                        
                        item_id_str = rental_parts[0]
                        date_str = rental_parts[1]
                        returned_str = rental_parts[2].lower() == 'true'
                        
                        # Parse date (format: MM/dd/yy)
                        try:
                            rental_date = datetime.strptime(date_str, '%m/%d/%y').date()
                        except:
                            rental_date = datetime.now().date()
                        
                        # Find item by legacy ID
                        try:
                            item = Item.objects.get(legacy_item_id=int(item_id_str))
                            
                            # Create rental record (simplified - no transaction link for historical data)
                            due_date = rental_date + timedelta(days=7)
                            return_date = rental_date if returned_str else None
                            
                            Rental.objects.create(
                                item=item,
                                customer=customer,
                                rental_date=rental_date,
                                due_date=due_date,
                                return_date=return_date,
                                is_returned=returned_str,
                                transaction=None  # Historical data without transaction
                            )
                        except Item.DoesNotExist:
                            print(f"  Item {item_id_str} not found, skipping rental")
                        except Exception as e:
                            print(f"  Error processing rental: {e}")
                    except Exception as e:
                        print(f"  Error parsing rental entry: {e}")
    
    print(f"Customer migration complete. Total: {Customer.objects.count()}")
    print(f"Rental migration complete. Total: {Rental.objects.count()}")


def migrate_coupons(legacy_path):
    """Migrate coupons from couponNumber.txt"""
    print("Migrating coupons...")
    
    with open(legacy_path, 'r') as f:
        for line in f:
            code = line.strip()
            if not code:
                continue
            
            # Skip if coupon already exists
            if Coupon.objects.filter(code=code).exists():
                print(f"  Skipping existing coupon: {code}")
                continue
            
            try:
                Coupon.objects.create(
                    code=code,
                    discount_percentage=Decimal('10.0'),  # Default 10% discount
                    is_active=True
                )
                print(f"  Migrated coupon: {code}")
            except Exception as e:
                print(f"  Error migrating coupon {code}: {e}")
    
    print(f"Coupon migration complete. Total: {Coupon.objects.count()}")


def main():
    """Main migration function"""
    print("=" * 60)
    print("Legacy Data Migration Script")
    print("=" * 60)
    
    # Path to legacy database files
    legacy_base_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '..',
        'Point-of-Sale-System-master',
        'Database'
    )
    
    if not os.path.exists(legacy_base_path):
        print(f"Error: Legacy database path not found: {legacy_base_path}")
        print("Please ensure the legacy system files are in the correct location.")
        return
    
    try:
        # Migrate employees
        employee_path = os.path.join(legacy_base_path, 'employeeDatabase.txt')
        if os.path.exists(employee_path):
            migrate_employees(employee_path)
        else:
            print(f"Warning: {employee_path} not found")
        
        # Migrate items
        item_path = os.path.join(legacy_base_path, 'itemDatabase.txt')
        if os.path.exists(item_path):
            migrate_items(item_path)
        else:
            print(f"Warning: {item_path} not found")
        
        # Migrate customers and rentals
        user_path = os.path.join(legacy_base_path, 'userDatabase.txt')
        if os.path.exists(user_path):
            migrate_customers_and_rentals(user_path)
        else:
            print(f"Warning: {user_path} not found")
        
        # Migrate coupons
        coupon_path = os.path.join(legacy_base_path, 'couponNumber.txt')
        if os.path.exists(coupon_path):
            migrate_coupons(coupon_path)
        else:
            print(f"Warning: {coupon_path} not found")
        
        print("\n" + "=" * 60)
        print("Migration Complete!")
        print("=" * 60)
        print(f"Total Employees: {Employee.objects.count()}")
        print(f"Total Items: {Item.objects.count()}")
        print(f"Total Customers: {Customer.objects.count()}")
        print(f"Total Rentals: {Rental.objects.count()}")
        print(f"Total Coupons: {Coupon.objects.count()}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

