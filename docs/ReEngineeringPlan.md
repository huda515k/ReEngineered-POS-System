# Software Reengineering Plan
## Legacy POS System to Modern Web-Based Application

### Project Overview
This document outlines the complete reengineering plan for transforming the legacy Java-based desktop Point-of-Sale (POS) system into a modern, web-based application following the Software Reengineering Process Model.

---

## Phase 1: Inventory Analysis

### 1.1 Code Assets Inventory

#### Core Business Logic Classes
- **POSSystem.java** - Main entry point, authentication, session management
- **PointOfSale.java** - Abstract base class for transaction types
- **POS.java** - Sale transaction handler
- **POR.java** - Rental transaction handler  
- **POH.java** - Return transaction handler
- **Inventory.java** - Inventory management (Singleton pattern)
- **Management.java** - User and rental management
- **Employee.java** - Employee entity
- **EmployeeManagement.java** - Employee CRUD operations
- **Item.java** - Item entity
- **ReturnItem.java** - Return item entity
- **Register.java** - Payment processing
- **Sale.java** - Sale operations
- **Rental.java** - Rental operations
- **HandleReturns.java** - Return processing

#### User Interface Classes
- **Login_Interface.java** - Authentication UI
- **Admin_Interface.java** - Admin dashboard
- **Cashier_Interface.java** - Cashier dashboard
- **Transaction_Interface.java** - Transaction UI
- **EnterItem_Interface.java** - Item entry UI
- **Payment_Interface.java** - Payment UI
- **AddEmployee_Interface.java** - Add employee UI
- **UpdateEmployee_Interface.java** - Update employee UI

#### Test Files
- **EmployeeTest.java**
- **EmployeeManagementTest.java**

### 1.2 Data Assets Inventory

#### Database Files (Plain Text)
- `employeeDatabase.txt` - Employee records (format: username position firstName lastName password)
- `itemDatabase.txt` - Item catalog (format: itemID itemName price quantity)
- `userDatabase.txt` - Customer/rental records (format: phoneNumber itemID,date,returned ...)
- `rentalDatabase.txt` - Rental items database
- `couponNumber.txt` - Valid coupon codes
- `saleInvoiceRecord.txt` - Sales transaction history
- `employeeLogfile.txt` - Employee login/logout audit trail
- `temp.txt` - Temporary transaction storage

### 1.3 Configuration Assets
- `build.xml` - Ant build configuration
- `manifest.mf` - JAR manifest
- `nbproject/` - NetBeans project configuration

### 1.4 Documentation Assets
- README.txt
- Documentation/ folder with various project documents

### 1.5 Asset Classification

#### Active Assets (To be migrated)
- All core business logic classes
- All data files
- Business rules and workflows

#### Obsolete Assets
- Desktop GUI classes (will be replaced with web UI)
- File-based data storage (will be replaced with database)
- OS-specific path handling code

#### Reusable Assets
- Business logic algorithms
- Data models (Employee, Item, Transaction concepts)
- Design patterns (Singleton, Abstract Factory)

### 1.6 Dependency Mapping

```
POSSystem
  ├── Employee
  ├── EmployeeManagement
  ├── PointOfSale (abstract)
  │   ├── POS (Sale)
  │   ├── POR (Rental)
  │   └── POH (Return)
  │       ├── Inventory (Singleton)
  │       ├── Item
  │       └── Management
  └── UI Classes (Login, Admin, Cashier, etc.)
```

---

## Phase 2: Document Restructuring

### 2.1 Legacy System Documentation

#### System Overview
The legacy system is a desktop-based POS application built with Java Swing. It supports:
- Employee authentication (Admin/Cashier roles)
- Sales transactions
- Rental transactions
- Return processing
- Inventory management
- Employee management

#### Architecture Diagram (Legacy)
```
┌─────────────────────────────────────────┐
│         GUI Layer (Swing)               │
│  Login | Admin | Cashier | Transaction │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Business Logic Layer                │
│  POSSystem | PointOfSale | Management   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Data Access Layer                   │
│  File I/O (Plain Text Files)            │
└─────────────────────────────────────────┘
```

#### Module Inventory
- **Authentication Module**: POSSystem, Login_Interface
- **Transaction Module**: POS, POR, POH, PointOfSale
- **Inventory Module**: Inventory, Item
- **User Management Module**: Management, Rental
- **Employee Management Module**: Employee, EmployeeManagement
- **Payment Module**: Register, Payment_Interface

---

## Phase 3: Reverse Engineering

### 3.1 Extracted Architecture

#### Current Design Patterns
1. **Singleton Pattern**: Inventory class
2. **Abstract Factory Pattern**: PointOfSale hierarchy (POS, POR, POH)
3. **Template Method Pattern**: PointOfSale abstract methods

#### Data Flow
1. User logs in → POSSystem validates credentials
2. Based on role → Redirect to Admin or Cashier interface
3. Transaction initiated → PointOfSale subclass handles it
4. Items added → Inventory checked and updated
5. Transaction completed → Data written to text files

### 3.2 Code Smells Identified

1. **God Class**: POSSystem contains too many responsibilities
2. **Long Method**: Management.addRental() and updateRentalStatus() are too long
3. **Duplicate Code**: File I/O operations repeated across classes
4. **Magic Numbers**: Hard-coded tax rates, discount values
5. **Primitive Obsession**: Using strings for dates, phone numbers
6. **Feature Envy**: Classes directly manipulating file paths
7. **Data Clumps**: Repeated file path handling code
8. **Comments**: Excessive commented-out code
9. **Dead Code**: Unused methods and variables
10. **Tight Coupling**: Direct file dependencies

### 3.3 Data Smells Identified

1. **Denormalized Data**: userDatabase.txt stores all rentals in one line
2. **No Data Validation**: No constraints on data format
3. **No Referential Integrity**: Item IDs referenced but not validated
4. **No Transactions**: No atomicity guarantees
5. **Poor Data Types**: Dates stored as strings (MM/dd/yy)
6. **No Indexing**: Sequential file reading for all queries
7. **Data Duplication**: Rental data duplicated across files
8. **No Backup Strategy**: Single point of failure

### 3.4 Current Limitations

1. **Scalability**: File-based storage doesn't scale
2. **Concurrency**: No support for multiple simultaneous users
3. **Data Integrity**: No ACID properties
4. **Performance**: Sequential file reads are slow
5. **Maintainability**: Tight coupling makes changes difficult
6. **Security**: Plain text passwords, no encryption
7. **Accessibility**: Desktop-only, no remote access
8. **Error Recovery**: Limited error handling and recovery

---

## Phase 4: Code Restructuring

### 4.1 Refactoring Strategy

#### Major Refactorings Planned

1. **Extract Repository Pattern**
   - Create data access layer abstraction
   - Remove direct file I/O from business logic

2. **Extract Service Layer**
   - Separate business logic from presentation
   - Create service classes for each domain

3. **Introduce DTOs**
   - Replace primitive data structures
   - Add proper data validation

4. **Extract Constants**
   - Move magic numbers to configuration
   - Centralize file paths

5. **Simplify Complex Methods**
   - Break down long methods
   - Extract helper methods

6. **Remove Code Duplication**
   - Create utility classes for common operations
   - Use inheritance and composition

---

## Phase 5: Data Restructuring

### 5.1 Database Schema Design

#### Normalized Relational Schema

**Tables:**
1. **employees**
   - id (PK, SERIAL)
   - username (UNIQUE, VARCHAR)
   - password_hash (VARCHAR) - encrypted
   - first_name (VARCHAR)
   - last_name (VARCHAR)
   - position (ENUM: 'Admin', 'Cashier')
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)

2. **items**
   - id (PK, SERIAL)
   - item_id (UNIQUE, INTEGER) - legacy ID
   - name (VARCHAR)
   - price (DECIMAL(10,2))
   - quantity (INTEGER)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)

3. **customers**
   - id (PK, SERIAL)
   - phone_number (UNIQUE, VARCHAR)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)

4. **transactions**
   - id (PK, SERIAL)
   - transaction_type (ENUM: 'Sale', 'Rental', 'Return')
   - employee_id (FK → employees.id)
   - customer_id (FK → customers.id, nullable)
   - total_amount (DECIMAL(10,2))
   - tax_rate (DECIMAL(5,4))
   - discount_applied (BOOLEAN)
   - coupon_code (VARCHAR, nullable)
   - created_at (TIMESTAMP)

5. **transaction_items**
   - id (PK, SERIAL)
   - transaction_id (FK → transactions.id)
   - item_id (FK → items.id)
   - quantity (INTEGER)
   - unit_price (DECIMAL(10,2))
   - subtotal (DECIMAL(10,2))

6. **rentals**
   - id (PK, SERIAL)
   - transaction_id (FK → transactions.id)
   - item_id (FK → items.id)
   - customer_id (FK → customers.id)
   - rental_date (DATE)
   - due_date (DATE)
   - return_date (DATE, nullable)
   - is_returned (BOOLEAN)
   - days_overdue (INTEGER, nullable)

7. **coupons**
   - id (PK, SERIAL)
   - code (UNIQUE, VARCHAR)
   - discount_percentage (DECIMAL(5,2))
   - is_active (BOOLEAN)
   - expires_at (TIMESTAMP, nullable)

8. **audit_logs**
   - id (PK, SERIAL)
   - employee_id (FK → employees.id)
   - action (VARCHAR) - 'login', 'logout', etc.
   - timestamp (TIMESTAMP)

### 5.2 Data Migration Plan

1. **Employee Migration**
   - Parse employeeDatabase.txt
   - Hash passwords (bcrypt)
   - Insert into employees table

2. **Item Migration**
   - Parse itemDatabase.txt
   - Insert into items table
   - Preserve legacy item_id

3. **Customer/Rental Migration**
   - Parse userDatabase.txt
   - Extract phone numbers → customers table
   - Parse rental entries → rentals table
   - Link to transactions

4. **Transaction History**
   - Parse saleInvoiceRecord.txt
   - Reconstruct transactions
   - Link transaction_items

5. **Coupon Migration**
   - Parse couponNumber.txt
   - Insert into coupons table

### 5.3 Database Choice Justification

**PostgreSQL** selected because:
- ACID compliance for transaction integrity
- Strong relational model support
- Excellent performance for POS workloads
- Robust indexing and query optimization
- JSON support for flexible data
- Excellent tooling and ecosystem
- Open source and widely supported

---

## Phase 6: Forward Engineering

### 6.1 Technology Stack Selection

#### Backend Framework: **Django (Python)**

**Justification:**
- Rapid development with built-in admin panel
- Excellent ORM for database abstraction
- Built-in authentication and security
- RESTful API support (Django REST Framework)
- Strong community and documentation
- Python's readability aids maintainability
- Excellent testing framework

#### Alternative Considered: Spring Boot (Java)
- Pros: Type safety, enterprise features
- Cons: More verbose, steeper learning curve for web development

#### Frontend: **React.js**

**Justification:**
- Component-based architecture
- Excellent state management
- Large ecosystem
- Modern UI/UX capabilities
- Strong community support

#### Database: **PostgreSQL**
(As justified in Phase 5)

### 6.2 Improved Architecture

#### Layered Architecture

```
┌─────────────────────────────────────────┐
│      Presentation Layer (React)         │
│  Components | State Management | API    │
└─────────────────┬───────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────┐
│      API Layer (Django REST Framework)   │
│  Views | Serializers | Permissions       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Business Logic Layer (Services)     │
│  TransactionService | InventoryService   │
│  EmployeeService | RentalService         │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Data Access Layer (Repositories)   │
│  Django ORM | Models | Migrations        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Database Layer (PostgreSQL)         │
│  Tables | Indexes | Constraints          │
└─────────────────────────────────────────┘
```

### 6.3 Design Patterns to Implement

1. **MVC Pattern**: Django's built-in MVC
2. **Repository Pattern**: Data access abstraction
3. **Service Layer Pattern**: Business logic encapsulation
4. **DTO Pattern**: Data transfer objects
5. **Factory Pattern**: Transaction type creation
6. **Strategy Pattern**: Payment methods
7. **Observer Pattern**: Audit logging
8. **Singleton Pattern**: Configuration management

### 6.4 Module Structure

```
pos_system/
├── backend/
│   ├── pos/
│   │   ├── models/          # Database models
│   │   ├── serializers/     # API serializers
│   │   ├── views/           # API views
│   │   ├── services/        # Business logic
│   │   ├── repositories/    # Data access
│   │   ├── utils/           # Utilities
│   │   └── migrations/      # Database migrations
│   ├── config/              # Settings
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/       # API clients
│   │   ├── store/          # State management
│   │   └── utils/          # Utilities
│   └── package.json
├── scripts/
│   ├── migrate_data.py      # Data migration script
│   └── seed_data.py        # Seed script
└── docs/                    # Documentation
```

### 6.5 Key Improvements

1. **Separation of Concerns**: Clear layer boundaries
2. **Database Integration**: Proper ORM with migrations
3. **API-First Design**: RESTful API for frontend
4. **Security**: Password hashing, CSRF protection, authentication
5. **Error Handling**: Comprehensive exception handling
6. **Logging**: Structured logging for debugging
7. **Testing**: Unit and integration tests
8. **Documentation**: API documentation, code comments
9. **Scalability**: Database-backed, stateless API
10. **Maintainability**: Modular, testable code

---

## Phase 7: Migration Strategy

### 7.1 Migration Timeline

1. **Week 1-2**: Inventory Analysis & Documentation
2. **Week 3**: Reverse Engineering & Smell Detection
3. **Week 4**: Code Restructuring (Legacy)
4. **Week 5-6**: Database Design & Data Migration
5. **Week 7-9**: Forward Engineering (Backend)
6. **Week 10-11**: Forward Engineering (Frontend)
7. **Week 12**: Testing, Integration, Deployment

### 7.2 Risk Analysis

#### Identified Risks

1. **Data Loss During Migration**
   - Mitigation: Comprehensive backup strategy, validation scripts

2. **Incomplete Feature Parity**
   - Mitigation: Detailed feature mapping, test cases

3. **Performance Issues**
   - Mitigation: Database indexing, query optimization, load testing

4. **Integration Challenges**
   - Mitigation: API versioning, gradual rollout

5. **Team Knowledge Gap**
   - Mitigation: Documentation, training sessions

### 7.3 Testing Strategy

1. **Unit Tests**: Business logic, services
2. **Integration Tests**: API endpoints, database operations
3. **Migration Tests**: Data integrity validation
4. **End-to-End Tests**: Complete user workflows
5. **Performance Tests**: Load testing, stress testing

---

## Phase 8: Deliverables

### 8.1 Technical Report
- Complete documentation of all phases
- Architecture diagrams (legacy and new)
- Refactoring documentation
- Technology justification
- Risk analysis

### 8.2 Reengineered System
- Modern web-based POS application
- Database schema and migrations
- API documentation
- Deployment instructions
- Test suite

---

## Conclusion

This reengineering plan provides a systematic approach to transforming the legacy POS system into a modern, maintainable, scalable web application while preserving all original functionality and improving architecture, data management, and user experience.

