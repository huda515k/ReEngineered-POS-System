"""
Database Backup Script
Creates automated backups of the database
"""
import os
import sys
import django
from datetime import datetime
import subprocess

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from django.conf import settings


def backup_sqlite(backup_dir):
    """Backup SQLite database"""
    db_path = settings.DATABASES['default']['NAME']
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found: {db_path}")
        return False
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{timestamp}.sqlite3"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copy database file
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ SQLite backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False


def backup_postgresql(backup_dir):
    """Backup PostgreSQL database"""
    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config.get('USER', 'postgres')
    db_host = db_config.get('HOST', 'localhost')
    db_port = db_config.get('PORT', '5432')
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Use pg_dump to create backup
        cmd = [
            'pg_dump',
            '-h', db_host,
            '-p', str(db_port),
            '-U', db_user,
            '-d', db_name,
            '-f', backup_path,
            '--no-password'  # Use .pgpass file for password
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PostgreSQL backup created: {backup_path}")
            return True
        else:
            print(f"❌ Error creating backup: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Error: pg_dump not found. Please install PostgreSQL client tools.")
        return False
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False


def cleanup_old_backups(backup_dir, keep_days=7):
    """Remove backups older than specified days"""
    if not os.path.exists(backup_dir):
        return
    
    from datetime import timedelta
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    
    deleted_count = 0
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff_date:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"  Deleted old backup: {filename}")
                except Exception as e:
                    print(f"  Error deleting {filename}: {e}")
    
    if deleted_count > 0:
        print(f"✅ Cleaned up {deleted_count} old backup(s)")


def main():
    """Main backup function"""
    print("=" * 60)
    print("Database Backup Script")
    print("=" * 60)
    
    # Determine backup directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(script_dir, '..', 'backups')
    backup_dir = os.path.abspath(backup_dir)
    
    # Get database engine
    db_engine = settings.DATABASES['default']['ENGINE']
    
    print(f"Database: {db_engine}")
    print(f"Backup directory: {backup_dir}")
    print()
    
    # Perform backup based on database type
    if 'sqlite' in db_engine:
        success = backup_sqlite(backup_dir)
    elif 'postgresql' in db_engine:
        success = backup_postgresql(backup_dir)
    else:
        print(f"❌ Unsupported database engine: {db_engine}")
        return
    
    if success:
        # Cleanup old backups (keep last 7 days)
        print("\nCleaning up old backups...")
        cleanup_old_backups(backup_dir, keep_days=7)
        
        print("\n" + "=" * 60)
        print("Backup Complete!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Backup Failed!")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()

