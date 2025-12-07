"""
Data Export Script
Exports database data to CSV or JSON format
"""
import os
import sys
import django
import csv
import json
from datetime import datetime

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos_app.models import Employee, Item, Customer, Transaction, Rental, Coupon, AuditLog


def export_to_csv(model_class, filename, fields=None):
    """Export model data to CSV"""
    queryset = model_class.objects.all()
    
    if not queryset.exists():
        print(f"  No data to export for {model_class.__name__}")
        return False
    
    # Get field names
    if fields is None:
        fields = [f.name for f in model_class._meta.get_fields() if f.concrete]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            
            for obj in queryset:
                row = {}
                for field in fields:
                    value = getattr(obj, field, None)
                    # Handle dates and foreign keys
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    elif hasattr(value, '__str__'):
                        value = str(value)
                    row[field] = value
                writer.writerow(row)
        
        print(f"  ✅ Exported {queryset.count()} {model_class.__name__} records to {filename}")
        return True
    except Exception as e:
        print(f"  ❌ Error exporting {model_class.__name__}: {e}")
        return False


def export_to_json(model_class, filename, fields=None):
    """Export model data to JSON"""
    queryset = model_class.objects.all()
    
    if not queryset.exists():
        print(f"  No data to export for {model_class.__name__}")
        return False
    
    # Get field names
    if fields is None:
        fields = [f.name for f in model_class._meta.get_fields() if f.concrete]
    
    try:
        data = []
        for obj in queryset:
            record = {}
            for field in fields:
                value = getattr(obj, field, None)
                # Handle dates and foreign keys
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                elif hasattr(value, '__str__'):
                    value = str(value)
                record[field] = value
            data.append(record)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Exported {len(data)} {model_class.__name__} records to {filename}")
        return True
    except Exception as e:
        print(f"  ❌ Error exporting {model_class.__name__}: {e}")
        return False


def main():
    """Main export function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export database data to CSV or JSON')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='csv',
                        help='Export format (default: csv)')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory (default: exports/)')
    parser.add_argument('--models', nargs='+', 
                        choices=['employees', 'items', 'customers', 'transactions', 
                                'rentals', 'coupons', 'audit_logs', 'all'],
                        default=['all'],
                        help='Models to export (default: all)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Data Export Script")
    print("=" * 60)
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, '..', 'exports')
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    print(f"Format: {args.format}")
    print()
    
    # Model mapping
    model_map = {
        'employees': Employee,
        'items': Item,
        'customers': Customer,
        'transactions': Transaction,
        'rentals': Rental,
        'coupons': Coupon,
        'audit_logs': AuditLog,
    }
    
    # Determine which models to export
    if 'all' in args.models:
        models_to_export = list(model_map.keys())
    else:
        models_to_export = args.models
    
    # Export each model
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for model_name in models_to_export:
        if model_name not in model_map:
            print(f"  ⚠️  Unknown model: {model_name}")
            continue
        
        model_class = model_map[model_name]
        base_filename = f"{model_name}_{timestamp}"
        
        if args.format in ['csv', 'both']:
            csv_filename = os.path.join(output_dir, f"{base_filename}.csv")
            export_to_csv(model_class, csv_filename)
        
        if args.format in ['json', 'both']:
            json_filename = os.path.join(output_dir, f"{base_filename}.json")
            export_to_json(model_class, json_filename)
    
    print("\n" + "=" * 60)
    print("Export Complete!")
    print("=" * 60)
    print(f"Files saved to: {output_dir}")


if __name__ == '__main__':
    main()

