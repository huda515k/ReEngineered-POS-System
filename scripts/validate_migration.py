"""
Migration Validation Script
Verifies that data migration from legacy system was successful
"""
import os
import sys
import django

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos_app.models import Employee, Item, Customer, Rental, Coupon, Transaction


def count_legacy_file_lines(file_path):
    """Count non-empty lines in legacy text file"""
    if not os.path.exists(file_path):
        return 0
    
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                count += 1
    return count


def validate_employees():
    """Validate employee migration"""
    print("Validating Employees...")
    
    legacy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'Point-of-Sale-System-master',
        'Database',
        'employeeDatabase.txt'
    )
    
    legacy_count = count_legacy_file_lines(legacy_path)
    db_count = Employee.objects.count()
    
    print(f"  Legacy file records: {legacy_count}")
    print(f"  Database records: {db_count}")
    
    if db_count >= legacy_count:
        print(f"  ✅ Employee migration validated")
        return True
    else:
        print(f"  ⚠️  Warning: Database has fewer employees than legacy file")
        return False


def validate_items():
    """Validate item migration"""
    print("Validating Items...")
    
    legacy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'Point-of-Sale-System-master',
        'Database',
        'itemDatabase.txt'
    )
    
    legacy_count = count_legacy_file_lines(legacy_path)
    db_count = Item.objects.count()
    
    print(f"  Legacy file records: {legacy_count}")
    print(f"  Database records: {db_count}")
    
    if db_count >= legacy_count:
        print(f"  ✅ Item migration validated")
        return True
    else:
        print(f"  ⚠️  Warning: Database has fewer items than legacy file")
        return False


def validate_customers():
    """Validate customer migration"""
    print("Validating Customers...")
    
    legacy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'Point-of-Sale-System-master',
        'Database',
        'userDatabase.txt'
    )
    
    # Count unique phone numbers in legacy file
    legacy_customers = set()
    if os.path.exists(legacy_path):
        with open(legacy_path, 'r') as f:
            next(f, None)  # Skip header
            for line in f:
                parts = line.strip().split()
                if parts:
                    legacy_customers.add(parts[0])
    
    legacy_count = len(legacy_customers)
    db_count = Customer.objects.count()
    
    print(f"  Legacy file unique customers: {legacy_count}")
    print(f"  Database records: {db_count}")
    
    if db_count >= legacy_count:
        print(f"  ✅ Customer migration validated")
        return True
    else:
        print(f"  ⚠️  Warning: Database has fewer customers than legacy file")
        return False


def validate_rentals():
    """Validate rental migration"""
    print("Validating Rentals...")
    
    legacy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'Point-of-Sale-System-master',
        'Database',
        'userDatabase.txt'
    )
    
    # Count rental entries in legacy file
    legacy_rentals = 0
    if os.path.exists(legacy_path):
        with open(legacy_path, 'r') as f:
            next(f, None)  # Skip header
            for line in f:
                parts = line.strip().split()
                if len(parts) > 1:
                    # Count rental entries (format: itemID,date,returned)
                    legacy_rentals += len(parts) - 1
    
    db_count = Rental.objects.count()
    
    print(f"  Legacy file rental entries: {legacy_rentals}")
    print(f"  Database records: {db_count}")
    
    if db_count >= legacy_rentals * 0.9:  # Allow 10% variance for normalization
        print(f"  ✅ Rental migration validated")
        return True
    else:
        print(f"  ⚠️  Warning: Database has significantly fewer rentals than legacy file")
        return False


def validate_coupons():
    """Validate coupon migration"""
    print("Validating Coupons...")
    
    legacy_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'Point-of-Sale-System-master',
        'Database',
        'couponNumber.txt'
    )
    
    legacy_count = count_legacy_file_lines(legacy_path)
    db_count = Coupon.objects.count()
    
    print(f"  Legacy file records: {legacy_count}")
    print(f"  Database records: {db_count}")
    
    if db_count >= legacy_count:
        print(f"  ✅ Coupon migration validated")
        return True
    else:
        print(f"  ⚠️  Warning: Database has fewer coupons than legacy file")
        return False


def validate_data_integrity():
    """Validate data integrity constraints"""
    print("Validating Data Integrity...")
    
    issues = []
    
    # Check for employees without usernames
    employees_no_username = Employee.objects.filter(username__isnull=True).count()
    if employees_no_username > 0:
        issues.append(f"  ⚠️  {employees_no_username} employees without username")
    
    # Check for items with negative prices
    items_negative_price = Item.objects.filter(price__lt=0).count()
    if items_negative_price > 0:
        issues.append(f"  ⚠️  {items_negative_price} items with negative prices")
    
    # Check for items with negative quantities
    items_negative_qty = Item.objects.filter(quantity__lt=0).count()
    if items_negative_qty > 0:
        issues.append(f"  ⚠️  {items_negative_qty} items with negative quantities")
    
    # Check for transactions without employees
    transactions_no_employee = Transaction.objects.filter(employee__isnull=True).count()
    if transactions_no_employee > 0:
        issues.append(f"  ⚠️  {transactions_no_employee} transactions without employee")
    
    # Check for rentals without items
    rentals_no_item = Rental.objects.filter(item__isnull=True).count()
    if rentals_no_item > 0:
        issues.append(f"  ⚠️  {rentals_no_item} rentals without item")
    
    if issues:
        for issue in issues:
            print(issue)
        return False
    else:
        print("  ✅ All data integrity checks passed")
        return True


def main():
    """Main validation function"""
    print("=" * 60)
    print("Migration Validation Script")
    print("=" * 60)
    print()
    
    results = []
    
    # Validate each data type
    results.append(("Employees", validate_employees()))
    print()
    results.append(("Items", validate_items()))
    print()
    results.append(("Customers", validate_customers()))
    print()
    results.append(("Rentals", validate_rentals()))
    print()
    results.append(("Coupons", validate_coupons()))
    print()
    results.append(("Data Integrity", validate_data_integrity()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\nOverall: {passed}/{total} validations passed")
    
    if passed == total:
        print("✅ Migration validation successful!")
        return 0
    else:
        print("⚠️  Some validations failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

