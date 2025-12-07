"""
Business Reports Generation Script
Generates various business reports from the database
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import csv

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos_app.models import Transaction, TransactionItem, Rental, Item, Employee, Customer
from django.db.models import Sum, Count, Avg, Q


def sales_report(start_date=None, end_date=None, output_file=None):
    """Generate sales report"""
    print("Generating Sales Report...")
    
    if start_date is None:
        start_date = datetime.now().date() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now().date()
    
    transactions = Transaction.objects.filter(
        transaction_type='Sale',
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    
    total_sales = transactions.aggregate(
        total=Sum('total_amount'),
        count=Count('id'),
        avg=Avg('total_amount')
    )
    
    print(f"  Period: {start_date} to {end_date}")
    print(f"  Total Sales: ${total_sales['total'] or 0:.2f}")
    print(f"  Number of Transactions: {total_sales['count']}")
    print(f"  Average Transaction: ${total_sales['avg'] or 0:.2f}")
    
    # Top selling items
    top_items = TransactionItem.objects.filter(
        transaction__in=transactions
    ).values('item__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('subtotal')
    ).order_by('-total_quantity')[:10]
    
    print("\n  Top 10 Selling Items:")
    for item in top_items:
        print(f"    {item['item__name']}: {item['total_quantity']} units, ${item['total_revenue']:.2f}")
    
    # Export to CSV if requested
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Transaction ID', 'Employee', 'Total Amount'])
            for txn in transactions:
                writer.writerow([
                    txn.created_at.date(),
                    txn.id,
                    txn.employee.username if txn.employee else 'N/A',
                    txn.total_amount
                ])
        print(f"\n  ✅ Report exported to {output_file}")
    
    return total_sales


def rental_report(start_date=None, end_date=None, output_file=None):
    """Generate rental report"""
    print("Generating Rental Report...")
    
    if start_date is None:
        start_date = datetime.now().date() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now().date()
    
    rentals = Rental.objects.filter(
        rental_date__gte=start_date,
        rental_date__lte=end_date
    )
    
    total_rentals = rentals.count()
    active_rentals = rentals.filter(is_returned=False).count()
    returned_rentals = rentals.filter(is_returned=True).count()
    overdue_rentals = rentals.filter(
        is_returned=False,
        due_date__lt=datetime.now().date()
    ).count()
    
    print(f"  Period: {start_date} to {end_date}")
    print(f"  Total Rentals: {total_rentals}")
    print(f"  Active Rentals: {active_rentals}")
    print(f"  Returned Rentals: {returned_rentals}")
    print(f"  Overdue Rentals: {overdue_rentals}")
    
    # Most rented items
    top_rented = rentals.values('item__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    print("\n  Top 10 Rented Items:")
    for item in top_rented:
        print(f"    {item['item__name']}: {item['count']} rentals")
    
    # Export to CSV if requested
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rental Date', 'Item', 'Customer', 'Due Date', 'Returned', 'Return Date'])
            for rental in rentals:
                writer.writerow([
                    rental.rental_date,
                    rental.item.name,
                    rental.customer.phone_number if rental.customer else 'N/A',
                    rental.due_date,
                    'Yes' if rental.is_returned else 'No',
                    rental.return_date or 'N/A'
                ])
        print(f"\n  ✅ Report exported to {output_file}")
    
    return {
        'total': total_rentals,
        'active': active_rentals,
        'returned': returned_rentals,
        'overdue': overdue_rentals
    }


def inventory_report(output_file=None):
    """Generate inventory report"""
    print("Generating Inventory Report...")
    
    items = Item.objects.all()
    total_items = items.count()
    low_stock_items = items.filter(quantity__lt=10)
    out_of_stock_items = items.filter(quantity=0)
    
    total_value = sum(item.price * item.quantity for item in items)
    
    print(f"  Total Items: {total_items}")
    print(f"  Total Inventory Value: ${total_value:.2f}")
    print(f"  Low Stock Items (< 10): {low_stock_items.count()}")
    print(f"  Out of Stock Items: {out_of_stock_items.count()}")
    
    print("\n  Low Stock Items:")
    for item in low_stock_items[:10]:
        print(f"    {item.name}: {item.quantity} units")
    
    # Export to CSV if requested
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Item ID', 'Name', 'Price', 'Quantity', 'Total Value', 'Status'])
            for item in items:
                status = 'Out of Stock' if item.quantity == 0 else \
                        'Low Stock' if item.quantity < 10 else 'In Stock'
                writer.writerow([
                    item.legacy_item_id,
                    item.name,
                    item.price,
                    item.quantity,
                    item.price * item.quantity,
                    status
                ])
        print(f"\n  ✅ Report exported to {output_file}")
    
    return {
        'total': total_items,
        'total_value': total_value,
        'low_stock': low_stock_items.count(),
        'out_of_stock': out_of_stock_items.count()
    }


def employee_performance_report(start_date=None, end_date=None, output_file=None):
    """Generate employee performance report"""
    print("Generating Employee Performance Report...")
    
    if start_date is None:
        start_date = datetime.now().date() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now().date()
    
    transactions = Transaction.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    
    employee_stats = transactions.values('employee__username', 'employee__first_name', 'employee__last_name').annotate(
        transaction_count=Count('id'),
        total_revenue=Sum('total_amount'),
        avg_transaction=Avg('total_amount')
    ).order_by('-total_revenue')
    
    print(f"  Period: {start_date} to {end_date}")
    print(f"\n  Employee Performance:")
    
    for stat in employee_stats:
        print(f"    {stat['employee__username']} ({stat['employee__first_name']} {stat['employee__last_name']}):")
        print(f"      Transactions: {stat['transaction_count']}")
        print(f"      Total Revenue: ${stat['total_revenue'] or 0:.2f}")
        print(f"      Avg Transaction: ${stat['avg_transaction'] or 0:.2f}")
    
    # Export to CSV if requested
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Employee', 'Username', 'Transactions', 'Total Revenue', 'Avg Transaction'])
            for stat in employee_stats:
                writer.writerow([
                    f"{stat['employee__first_name']} {stat['employee__last_name']}",
                    stat['employee__username'],
                    stat['transaction_count'],
                    stat['total_revenue'] or 0,
                    stat['avg_transaction'] or 0
                ])
        print(f"\n  ✅ Report exported to {output_file}")
    
    return employee_stats


def main():
    """Main report generation function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate business reports')
    parser.add_argument('--report', choices=['sales', 'rental', 'inventory', 'employee', 'all'],
                        default='all', help='Type of report to generate')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--output-dir', default=None, help='Output directory for CSV files')
    
    args = parser.parse_args()
    
    # Parse dates
    start_date = None
    end_date = None
    
    if args.start_date:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
    if args.end_date:
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, '..', 'reports')
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Business Reports Generation")
    print("=" * 60)
    print()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if args.report in ['sales', 'all']:
        output_file = os.path.join(output_dir, f'sales_report_{timestamp}.csv') if args.output_dir or True else None
        sales_report(start_date, end_date, output_file)
        print()
    
    if args.report in ['rental', 'all']:
        output_file = os.path.join(output_dir, f'rental_report_{timestamp}.csv') if args.output_dir or True else None
        rental_report(start_date, end_date, output_file)
        print()
    
    if args.report in ['inventory', 'all']:
        output_file = os.path.join(output_dir, f'inventory_report_{timestamp}.csv') if args.output_dir or True else None
        inventory_report(output_file)
        print()
    
    if args.report in ['employee', 'all']:
        output_file = os.path.join(output_dir, f'employee_report_{timestamp}.csv') if args.output_dir or True else None
        employee_performance_report(start_date, end_date, output_file)
        print()
    
    print("=" * 60)
    print("Report Generation Complete!")
    print("=" * 60)
    if args.output_dir or True:
        print(f"Reports saved to: {output_dir}")


if __name__ == '__main__':
    main()

