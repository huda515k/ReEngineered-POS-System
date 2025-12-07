# Deployment Guide
## Reengineered POS System

This guide provides comprehensive instructions for deploying the reengineered POS system in both development and production environments.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Development Environment Setup](#2-development-environment-setup)
3. [Production Environment Setup](#3-production-environment-setup)
4. [Database Setup](#4-database-setup)
5. [Backend Deployment](#5-backend-deployment)
6. [Frontend Deployment](#6-frontend-deployment)
7. [Final Integration Testing](#7-final-integration-testing)
8. [Troubleshooting](#8-troubleshooting)
9. [Post-Deployment Checklist](#9-post-deployment-checklist)

---

## 1. Prerequisites

### System Requirements

**Minimum Requirements:**
- **OS**: Linux (Ubuntu 20.04+), macOS 10.15+, or Windows 10+
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 10GB free space
- **Network**: Internet connection for package installation

**Recommended Requirements:**
- **OS**: Linux (Ubuntu 22.04 LTS) or macOS 12+
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 20GB+ free space (SSD recommended)

### Software Prerequisites

**Backend:**
- Python 3.10 or higher
- pip (Python package manager)
- PostgreSQL 14+ (for production) or SQLite3 (for development)
- Virtual environment tool (venv)

**Frontend:**
- Node.js 18.0 or higher
- npm 9.0 or higher (comes with Node.js)

**Database (Production):**
- PostgreSQL 14+ server
- Database user with create database privileges

**Additional Tools:**
- Git (for version control)
- Text editor or IDE (VS Code, PyCharm, etc.)

### Verify Prerequisites

```bash
# Check Python version
python3 --version  # Should be 3.10+

# Check Node.js version
node --version  # Should be 18.0+

# Check npm version
npm --version  # Should be 9.0+

# Check PostgreSQL (if using)
psql --version  # Should be 14.0+

# Check Git
git --version
```

---

## 2. Development Environment Setup

### 2.1 Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd "SRe Project/reengineered_pos_system"
```

### 2.2 Backend Setup

#### Step 1: Create Virtual Environment

```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Note**: For PostgreSQL support, uncomment `psycopg2-binary==2.9.9` in `requirements.txt` and install:
```bash
pip install psycopg2-binary==2.9.9
```

#### Step 3: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
touch .env
```

Add the following to `.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (for PostgreSQL)
DB_NAME=pos_system
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

**Generate Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Step 4: Run Database Migrations

```bash
# For SQLite (development)
python manage.py migrate

# For PostgreSQL (see Database Setup section)
# python manage.py migrate
```

#### Step 5: Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

#### Step 6: Load Initial Data (Optional)

```bash
# If you have fixtures
python manage.py loaddata initial_data.json

# Or run data migration script
cd ../scripts
python migrate_data.py
```

#### Step 7: Start Development Server

```bash
cd backend
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### 2.3 Frontend Setup

#### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

#### Step 2: Configure API Endpoint

Verify `package.json` has the correct proxy:
```json
{
  "proxy": "http://localhost:8000"
}
```

#### Step 3: Start Development Server

```bash
npm start
```

Frontend will be available at `http://localhost:3000`

---

## 3. Production Environment Setup

### 3.1 Server Preparation

#### Update System Packages

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx nodejs npm git
```

### 3.2 Security Configuration

#### Create Application User

```bash
# Create non-root user for application
sudo adduser posapp
sudo usermod -aG sudo posapp
su - posapp
```

#### Configure Firewall

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 4. Database Setup

### 4.1 PostgreSQL Installation (Production)

#### Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS (using Homebrew)
brew install postgresql@14
brew services start postgresql@14

# Windows
# Download installer from https://www.postgresql.org/download/windows/
```

#### Verify Installation

```bash
sudo systemctl status postgresql  # Linux
# or
psql --version
```

### 4.2 Create Database and User

#### Step 1: Access PostgreSQL

```bash
sudo -u postgres psql
```

#### Step 2: Create Database and User

```sql
-- Create database
CREATE DATABASE pos_system;

-- Create user
CREATE USER pos_user WITH PASSWORD 'your-secure-password-here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE pos_system TO pos_user;

-- Grant schema privileges (PostgreSQL 15+)
\c pos_system
GRANT ALL ON SCHEMA public TO pos_user;

-- Exit
\q
```

#### Step 3: Configure PostgreSQL Authentication

Edit `/etc/postgresql/14/main/pg_hba.conf` (path may vary):

```conf
# Add or modify this line
local   all             pos_user                              md5
host    all             pos_user      127.0.0.1/32          md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### 4.3 Configure Django for PostgreSQL

#### Step 1: Update `requirements.txt`

Uncomment PostgreSQL driver:
```txt
psycopg2-binary==2.9.9
```

Install:
```bash
pip install psycopg2-binary==2.9.9
```

#### Step 2: Update `settings.py`

In `backend/pos_system/settings.py`, uncomment PostgreSQL configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='pos_system'),
        'USER': config('DB_USER', default='pos_user'),
        'PASSWORD': config('DB_PASSWORD', default='your-secure-password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

#### Step 3: Update `.env` File

```env
DB_NAME=pos_system
DB_USER=pos_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

#### Step 4: Run Migrations

```bash
cd backend
source venv/bin/activate
python manage.py migrate
```

### 4.4 Database Backup Configuration

#### Create Backup Script

Create `scripts/backup_database.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/pos_system"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="pos_system"
DB_USER="pos_user"

mkdir -p $BACKUP_DIR

pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "Backup completed: backup_$DATE.sql"
```

Make executable:
```bash
chmod +x scripts/backup_database.sh
```

#### Schedule Automated Backups

Add to crontab:
```bash
crontab -e

# Add this line (daily backup at 2 AM)
0 2 * * * /path/to/scripts/backup_database.sh
```

---

## 5. Backend Deployment

### 5.1 Production Settings

#### Update `settings.py` for Production

```python
# Security settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'your-server-ip']

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files (if needed)
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

#### Update `.env` for Production

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 5.2 Collect Static Files

```bash
cd backend
python manage.py collectstatic --noinput
```

### 5.3 Setup Gunicorn (WSGI Server)

#### Install Gunicorn

```bash
pip install gunicorn
```

#### Create Gunicorn Configuration

Create `backend/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
preload_app = True
```

#### Test Gunicorn

```bash
cd backend
gunicorn --config gunicorn_config.py pos_system.wsgi:application
```

### 5.4 Setup Systemd Service

Create `/etc/systemd/system/pos-backend.service`:

```ini
[Unit]
Description=POS System Backend (Gunicorn)
After=network.target postgresql.service

[Service]
User=posapp
Group=posapp
WorkingDirectory=/home/posapp/reengineered_pos_system/backend
Environment="PATH=/home/posapp/reengineered_pos_system/backend/venv/bin"
ExecStart=/home/posapp/reengineered_pos_system/backend/venv/bin/gunicorn \
    --config /home/posapp/reengineered_pos_system/backend/gunicorn_config.py \
    pos_system.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable pos-backend
sudo systemctl start pos-backend
sudo systemctl status pos-backend
```

---

## 6. Frontend Deployment

### 6.1 Build Production Bundle

```bash
cd frontend
npm run build
```

This creates an optimized production build in the `build/` directory.

### 6.2 Configure Nginx

#### Install Nginx

```bash
sudo apt install nginx
```

#### Create Nginx Configuration

Create `/etc/nginx/sites-available/pos-system`:

```nginx
# Backend API
upstream pos_backend {
    server 127.0.0.1:8000;
}

# Frontend
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS (if using SSL)
    # return 301 https://$server_name$request_uri;

    # Frontend static files
    location / {
        root /home/posapp/reengineered_pos_system/frontend/build;
        try_files $uri $uri/ /index.html;
        index index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://pos_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /home/posapp/reengineered_pos_system/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files (if needed)
    location /media/ {
        alias /home/posapp/reengineered_pos_system/backend/media/;
        expires 7d;
    }
}

# HTTPS Configuration (if using SSL)
# server {
#     listen 443 ssl http2;
#     server_name your-domain.com www.your-domain.com;
#
#     ssl_certificate /path/to/certificate.crt;
#     ssl_certificate_key /path/to/private.key;
#
#     # SSL configuration
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers HIGH:!aNULL:!MD5;
#     ssl_prefer_server_ciphers on;
#
#     # Same location blocks as above
# }
```

#### Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/pos-system /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### 6.3 SSL Certificate (Optional but Recommended)

#### Using Let's Encrypt (Certbot)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Certbot will automatically configure Nginx for SSL.

---

## 7. Final Integration Testing

### 7.1 Pre-Deployment Testing Checklist

#### Backend API Testing

```bash
cd backend
source venv/bin/activate

# Run all tests
python manage.py test

# Run specific test suites
python manage.py test pos_app.tests.test_models
python manage.py test pos_app.tests.test_services
python manage.py test pos_app.tests.test_views
```

**Expected Results:**
- All tests should pass (29+ tests)
- No errors or warnings

#### Database Connection Test

```bash
python manage.py dbshell
# Should connect successfully
# Type \q to exit
```

#### Static Files Collection Test

```bash
python manage.py collectstatic --noinput --dry-run
# Should list all static files to be collected
```

### 7.2 Integration Test Scenarios

#### Test 1: Authentication Flow

1. **Start Services:**
   ```bash
   # Backend
   sudo systemctl status pos-backend
   
   # Frontend (if running separately)
   # Or access via Nginx
   ```

2. **Test Login:**
   - Navigate to `http://your-domain.com` (or `http://localhost:3000` in dev)
   - Attempt login with valid credentials
   - Verify successful authentication
   - Check session persistence

3. **Test Logout:**
   - Click logout
   - Verify session cleared
   - Verify redirect to login page

**Expected Results:**
- Login successful
- Session maintained
- Logout clears session

#### Test 2: Transaction Processing

1. **Create Sale Transaction:**
   - Login as Cashier
   - Add items to cart
   - Apply discount (if applicable)
   - Process payment
   - Verify transaction saved

2. **Create Rental Transaction:**
   - Login as Cashier
   - Select rental option
   - Add rental items
   - Enter customer phone number
   - Process rental
   - Verify rental records created

3. **Process Return:**
   - Login as Cashier
   - Select return option
   - Enter rental ID or customer phone
   - Process return
   - Verify inventory updated

**Expected Results:**
- All transactions processed successfully
- Database records created correctly
- Inventory updated accurately

#### Test 3: Inventory Management

1. **View Inventory:**
   - Login as Admin or Cashier
   - Navigate to inventory
   - Verify all items displayed
   - Check quantities accurate

2. **Update Inventory:**
   - Login as Admin
   - Update item quantity
   - Verify change saved
   - Check quantity reflected in transactions

**Expected Results:**
- Inventory displays correctly
- Updates persist
- Quantities accurate

#### Test 4: Employee Management (Admin Only)

1. **View Employees:**
   - Login as Admin
   - Navigate to employee management
   - Verify employee list displayed

2. **Add Employee:**
   - Create new employee
   - Set username, password, position
   - Save employee
   - Verify employee can login

3. **Update Employee:**
   - Edit existing employee
   - Update information
   - Verify changes saved

4. **Deactivate Employee:**
   - Deactivate employee
   - Verify employee cannot login

**Expected Results:**
- All CRUD operations work
- Permissions enforced
- Changes persist

#### Test 5: API Endpoint Testing

Use curl or Postman to test API endpoints:

```bash
# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'

# Test inventory endpoint (requires authentication)
curl -X GET http://localhost:8000/api/inventory/ \
  -H "Authorization: Session <session-id>"

# Test transaction creation
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Session <session-id>" \
  -d '{"transaction_type":"Sale","items":[...]}'
```

**Expected Results:**
- All endpoints respond correctly
- Authentication required where needed
- Data returned in correct format

### 7.3 Database Integration Tests

#### Test Database Connectivity

```bash
python manage.py dbshell
```

Run SQL queries:
```sql
-- Check tables exist
\dt

-- Check employee count
SELECT COUNT(*) FROM pos_app_employee;

-- Check item count
SELECT COUNT(*) FROM pos_app_item;

-- Check transaction count
SELECT COUNT(*) FROM pos_app_transaction;
```

#### Test Data Integrity

```bash
python manage.py check --deploy
```

**Expected Results:**
- All checks pass
- No warnings about production settings

### 7.4 Performance Testing

#### Test Response Times

```bash
# Install Apache Bench (ab)
sudo apt install apache2-utils

# Test API response time
ab -n 100 -c 10 http://localhost:8000/api/inventory/
```

**Expected Results:**
- Response time < 200ms for most endpoints
- No errors under normal load

### 7.5 Security Testing

#### Test Authentication

1. Attempt to access protected endpoints without authentication
2. Verify 401/403 responses

#### Test Input Validation

1. Submit invalid data to forms
2. Verify validation errors displayed
3. Verify no SQL injection possible

#### Test CORS Configuration

Verify CORS headers configured correctly for production.

---

## 8. Troubleshooting

### Common Issues and Solutions

#### Issue 1: Database Connection Failed

**Symptoms:**
- `django.db.utils.OperationalError: could not connect to server`

**Solutions:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U pos_user -d pos_system -h localhost

# Verify credentials in .env file
# Check pg_hba.conf configuration
```

#### Issue 2: Static Files Not Loading

**Symptoms:**
- CSS/JS files return 404

**Solutions:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t

# Verify static file paths in settings.py
```

#### Issue 3: CORS Errors

**Symptoms:**
- Frontend cannot connect to backend API

**Solutions:**
```python
# Update CORS settings in settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "http://localhost:3000",
]
```

#### Issue 4: Gunicorn Not Starting

**Symptoms:**
- Service fails to start

**Solutions:**
```bash
# Check logs
sudo journalctl -u pos-backend -n 50

# Verify virtual environment path
# Check file permissions
# Verify gunicorn_config.py exists
```

#### Issue 5: Migration Errors

**Symptoms:**
- `django.db.migrations.exceptions.MigrationConflict`

**Solutions:**
```bash
# Check migration status
python manage.py showmigrations

# Reset migrations (development only)
python manage.py migrate --fake-initial

# For production, review migration files
```

---

## 9. Post-Deployment Checklist

### Immediate Post-Deployment

- [ ] All services running (backend, frontend, database, nginx)
- [ ] Database migrations applied successfully
- [ ] Static files collected
- [ ] Superuser account created
- [ ] Initial data loaded (if applicable)
- [ ] SSL certificate installed (if using HTTPS)
- [ ] Firewall configured correctly

### Functionality Verification

- [ ] User authentication working
- [ ] Sales transactions processing
- [ ] Rental transactions processing
- [ ] Return processing working
- [ ] Inventory management functional
- [ ] Employee management working (Admin)
- [ ] Audit logging active
- [ ] Reports generating correctly

### Performance Verification

- [ ] API response times acceptable (< 200ms)
- [ ] Page load times acceptable (< 2s)
- [ ] Database queries optimized
- [ ] Static files cached properly

### Security Verification

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is secure and not in version control
- [ ] HTTPS enabled (if applicable)
- [ ] CORS configured correctly
- [ ] Authentication required for protected endpoints
- [ ] Input validation working
- [ ] SQL injection protection verified

### Monitoring Setup

- [ ] Error logging configured
- [ ] Database backup scheduled
- [ ] System monitoring tools installed (optional)
- [ ] Uptime monitoring configured (optional)

### Documentation

- [ ] Deployment documentation complete
- [ ] API documentation accessible
- [ ] User manual available
- [ ] Troubleshooting guide created

---

## Additional Resources

### Useful Commands

```bash
# View backend logs
sudo journalctl -u pos-backend -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Restart services
sudo systemctl restart pos-backend
sudo systemctl restart nginx
sudo systemctl restart postgresql

# Check service status
sudo systemctl status pos-backend
sudo systemctl status nginx
sudo systemctl status postgresql
```

### Support Contacts

- **Technical Issues**: [Your support email]
- **Documentation**: [Documentation URL]
- **Repository**: [Git repository URL]

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Maintained By**: Development Team

