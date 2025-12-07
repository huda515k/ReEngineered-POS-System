# POS System Frontend

React.js frontend for the reengineered POS system.

## Setup

```bash
npm install
npm start
```

The frontend will run on http://localhost:3000 and proxy API requests to http://localhost:8000

## Features

- Employee authentication (Login/Logout)
- Sales transactions
- Rental transactions
- Return processing
- Inventory management
- Employee management (Admin only)

## API Endpoints

All API endpoints are prefixed with `/api/` and require authentication (except login):

### Authentication
- `POST /api/auth/login/` - Employee login
- `POST /api/auth/logout/` - Employee logout

### Items
- `GET /api/items/` - List/search items (query param: `?search=query`)
- `GET /api/items/{id}/` - Get item details

### Transactions
- `GET /api/transactions/` - List all transactions
- `GET /api/transactions/{id}/` - Get transaction details
- `POST /api/transactions/sale/` - Create sale transaction
- `POST /api/transactions/rental/` - Create rental transaction
- `POST /api/transactions/return/` - Process return transaction
- `GET /api/transactions/outstanding-rentals/` - Get outstanding rentals (query param: `?customer_phone=1234567890`)

### Employees (Admin only)
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee

### API Root
- `GET /` - API root with endpoint documentation

