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

All API endpoints are prefixed with `/api/`:
- `/api/auth/login/` - Employee login
- `/api/auth/logout/` - Employee logout
- `/api/items/` - List/search items
- `/api/transactions/` - List transactions
- `/api/transactions/sale/` - Create sale
- `/api/transactions/rental/` - Create rental
- `/api/transactions/return/` - Process return
- `/api/employees/` - Employee management (Admin only)

