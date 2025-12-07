"""
Data Cleanup Script
Archives or removes old records based on specified criteria
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos_app.models import Transaction, Rental, AuditLog


def archive_old_transactions(days=365, dry_run=True):
    """Archive transactions older than specified days"""
    cutoff_date = datetime.now().date() - timedelta(days=days)
    
    old_transactions = Transaction.objects.filter(created_at__lt=cutoff_date)
    count = old_transactions.count()
    
    print(f"Found {count} transactions older than {days} days (before {cutoff_date})")
    
    if dry_run:
        print("  [DRY RUN] Would archive these transactions")
        return 0
    
    # In a real implementation, you might:
    # 1. Export to archive file
    # 2. Move to archive table
    # 3. Delete (if confirmed)
    
    print("  ⚠️  Archive functionality not implemented. Use export_data.py to backup first.")
    return 0


def cleanup_returned_rentals(days=90, dry_run=True):
    """Remove old returned rental records"""
    cutoff_date = datetime.now().date() - timedelta(days=days)
    
    old_rentals = Rental.objects.filter(
        is_returned=True,
        return_date__lt=cutoff_date
    )
    count = old_rentals.count()
    
    print(f"Found {count} returned rentals older than {days} days (returned before {cutoff_date})")
    
    if dry_run:
        print("  [DRY RUN] Would delete these rentals")
        return 0
    
    deleted = old_rentals.delete()[0]
    print(f"  ✅ Deleted {deleted} old rental records")
    return deleted


def cleanup_old_audit_logs(days=180, dry_run=True):
    """Remove old audit log entries"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    old_logs = AuditLog.objects.filter(timestamp__lt=cutoff_date)
    count = old_logs.count()
    
    print(f"Found {count} audit log entries older than {days} days (before {cutoff_date})")
    
    if dry_run:
        print("  [DRY RUN] Would delete these audit logs")
        return 0
    
    deleted = old_logs.delete()[0]
    print(f"  ✅ Deleted {deleted} old audit log entries")
    return deleted


def cleanup_orphaned_records(dry_run=True):
    """Remove orphaned records (records with broken foreign keys)"""
    print("Checking for orphaned records...")
    
    issues = []
    
    # Check for rentals without valid items
    orphaned_rentals = Rental.objects.filter(item__isnull=True)
    count = orphaned_rentals.count()
    if count > 0:
        issues.append(("Orphaned rentals (no item)", orphaned_rentals, dry_run))
    
    # Check for rentals without valid customers
    orphaned_rentals = Rental.objects.filter(customer__isnull=True)
    count = orphaned_rentals.count()
    if count > 0:
        issues.append(("Orphaned rentals (no customer)", orphaned_rentals, dry_run))
    
    # Check for transaction items without valid transactions
    from pos_app.models import TransactionItem
    orphaned_items = TransactionItem.objects.filter(transaction__isnull=True)
    count = orphaned_items.count()
    if count > 0:
        issues.append(("Orphaned transaction items", orphaned_items, dry_run))
    
    if not issues:
        print("  ✅ No orphaned records found")
        return 0
    
    total_deleted = 0
    for name, queryset, is_dry_run in issues:
        count = queryset.count()
        print(f"  Found {count} {name}")
        
        if is_dry_run:
            print(f"    [DRY RUN] Would delete these records")
        else:
            deleted = queryset.delete()[0]
            print(f"    ✅ Deleted {deleted} records")
            total_deleted += deleted
    
    return total_deleted


def main():
    """Main cleanup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cleanup old data from database')
    parser.add_argument('--transactions-days', type=int, default=365,
                        help='Archive transactions older than N days (default: 365)')
    parser.add_argument('--rentals-days', type=int, default=90,
                        help='Delete returned rentals older than N days (default: 90)')
    parser.add_argument('--audit-logs-days', type=int, default=180,
                        help='Delete audit logs older than N days (default: 180)')
    parser.add_argument('--orphaned', action='store_true',
                        help='Clean up orphaned records')
    parser.add_argument('--execute', action='store_true',
                        help='Actually perform cleanup (default is dry-run)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Data Cleanup Script")
    print("=" * 60)
    
    if not args.execute:
        print("⚠️  DRY RUN MODE - No data will be deleted")
        print("   Use --execute flag to perform actual cleanup")
    print()
    
    dry_run = not args.execute
    
    # Perform cleanup operations
    print("1. Transaction Cleanup")
    archive_old_transactions(days=args.transactions_days, dry_run=dry_run)
    print()
    
    print("2. Rental Cleanup")
    cleanup_returned_rentals(days=args.rentals_days, dry_run=dry_run)
    print()
    
    print("3. Audit Log Cleanup")
    cleanup_old_audit_logs(days=args.audit_logs_days, dry_run=dry_run)
    print()
    
    if args.orphaned:
        print("4. Orphaned Records Cleanup")
        cleanup_orphaned_records(dry_run=dry_run)
        print()
    
    print("=" * 60)
    if dry_run:
        print("Dry run complete. Use --execute to perform actual cleanup.")
    else:
        print("Cleanup complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()

