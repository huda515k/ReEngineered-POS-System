# Reengineered POS System

Modern web-based Point-of-Sale system reengineered from legacy Java desktop application.

## Technology Stack

- **Backend**: Django 4.2+ (Python 3.10+)
- **Frontend**: React.js 18+
- **Database**: PostgreSQL 14+
- **API**: Django REST Framework

## Project Structure

```
reengineered_pos_system/
├── backend/          # Django backend application
├── frontend/         # React frontend application
├── scripts/          # Migration and utility scripts
└── docs/            # Documentation

```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- pip and npm

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

### Database Migration from Legacy System

```bash
cd scripts
python migrate_data.py
```

## Features

- Employee authentication (Admin/Cashier roles)
- Sales transactions
- Rental transactions
- Return processing
- Inventory management
- Employee management
- Real-time inventory updates
- Transaction history
- Audit logging

## API Documentation

API documentation available at `/api/docs/` when backend is running.

## Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

