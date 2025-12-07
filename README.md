# ReEngineered-POS-System

**Legacy Java POS System → Modern Web Application**

A complete software reengineering project transforming a legacy Java Swing desktop Point-of-Sale (POS) system into a modern, scalable web application using Django REST Framework and React.js. Features role-based access control, real-time inventory management, and comprehensive transaction processing.

## 🎯 Project Overview

This project documents the complete reengineering of a legacy Java-based desktop Point-of-Sale (POS) system into a modern, web-based application. The transformation follows the Software Reengineering Process Model, systematically improving architecture, data management, security, and user experience while preserving all original functionality.

## 🔄 Transformation Summary

**From:**
- Legacy Java Swing desktop application
- File-based data storage (plain text files)
- Monolithic architecture
- Single-user system
- Plain text password storage

**To:**
- Modern React.js web application
- PostgreSQL database with normalized schema
- Layered architecture (5 layers)
- Multi-user concurrent access
- Secure authentication (bcrypt hashing)

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 4.2+ with Django REST Framework
- **Database:** PostgreSQL 14+ (SQLite for development)
- **Language:** Python 3.9+
- **Authentication:** Session-based with bcrypt password hashing

### Frontend
- **Framework:** React.js 18+
- **Routing:** React Router 6+
- **HTTP Client:** Axios
- **Styling:** Modern CSS with responsive design

## ✨ Key Features

- ✅ **Role-Based Access Control:** Admin and Cashier roles with different permissions
- ✅ **Transaction Processing:** Sales, Rentals, and Returns
- ✅ **Inventory Management:** Real-time stock tracking and updates
- ✅ **Employee Management:** CRUD operations (Admin only)
- ✅ **Transaction History:** Complete audit trail of all transactions
- ✅ **Customer Management:** Automatic customer creation and tracking
- ✅ **Coupon System:** Discount code validation and application
- ✅ **Audit Logging:** Comprehensive activity tracking

## 📁 Project Structure

```
reengineered_pos_system/
├── backend/                 # Django backend
│   ├── pos_app/            # Main application
│   │   ├── models/         # Database models
│   │   ├── serializers/    # API serializers
│   │   ├── views/          # API endpoints
│   │   ├── services/       # Business logic
│   │   └── tests/          # Test suite (39 tests)
│   └── pos_system/         # Project settings
├── frontend/                # React frontend
│   └── src/
│       ├── components/     # React components
│       └── services/       # API clients
├── docs/                    # Comprehensive documentation
│   ├── TECHNICAL_REPORT.md
│   ├── REFACTORING_DOCUMENTATION.md
│   ├── LEGACY_VS_REENGINEERED_COMPARISON.md
│   └── WORK_DISTRIBUTION.md
└── scripts/                 # Utility scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+ (optional, SQLite used by default)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Default Credentials
- **Admin:** `110001` / `1`
- **Cashier:** `110002` / `lehigh2016`

## 📊 Reengineering Phases

1. **Phase 1:** Inventory Analysis
2. **Phase 2:** Document Restructuring
3. **Phase 3:** Reverse Engineering
4. **Phase 4:** Code Restructuring
5. **Phase 5:** Data Restructuring
6. **Phase 6:** Forward Engineering
7. **Phase 7:** Migration Strategy
8. **Phase 8:** Testing & Quality Assurance
9. **Phase 9:** Documentation

## 🧪 Testing

- **Total Tests:** 39 automated tests
- **Coverage:** Models, Services, Views, Migration
- **Status:** All tests passing ✅

Run tests:
```bash
cd backend
python manage.py test
```

## 📚 Documentation

Comprehensive documentation available in the `docs/` directory:
- **Technical Report** - Complete project documentation
- **Refactoring Documentation** - 9 refactorings with before/after code
- **Legacy vs Re-engineered Comparison** - Detailed comparison with diagrams
- **Work Distribution** - Team member responsibilities
- **Deployment Guide** - Production deployment instructions
- **Quick Start Guide** - Getting started guide

## 🏗️ Architecture

### Legacy System
- 3-layer monolithic architecture
- File-based storage
- Desktop-only deployment

### Re-engineered System
- 5-layer architecture (Presentation, API, Business Logic, Data Access, Database)
- Database-backed with ACID properties
- Web-based, accessible from anywhere

## 🔒 Security Improvements

- ✅ Bcrypt password hashing (replaces plain text)
- ✅ CSRF protection
- ✅ XSS protection
- ✅ SQL injection prevention (ORM)
- ✅ Session-based authentication
- ✅ Role-based access control

## 📈 Performance Improvements

- **Query Performance:** 10-100x faster (indexed database vs sequential file reads)
- **Scalability:** Unlimited users (vs single user)
- **Concurrency:** Multi-user support with database transactions

## 👥 Team

- **Huda:** Phases 1, 3, 4, 7, 9 (Lead)
- **Umer:** Phases 2, 4, 5, 7, 8 (Lead)
- **Moawiz:** Phases 4, 6, 8, 9 (Lead)

## 🙏 Acknowledgments

This project demonstrates modern software reengineering practices, transforming legacy systems into maintainable, scalable applications.
