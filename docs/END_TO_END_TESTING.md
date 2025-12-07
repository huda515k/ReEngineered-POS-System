# End-to-End Testing Documentation
## Reengineered POS System

This document provides comprehensive end-to-end testing procedures, performance testing guidelines, and user acceptance testing scenarios for the reengineered POS system.

---

## Table of Contents

1. [Overview](#1-overview)
2. [End-to-End Testing](#2-end-to-end-testing)
3. [Performance Testing](#3-performance-testing)
4. [User Acceptance Testing](#4-user-acceptance-testing)
5. [Test Execution Plan](#5-test-execution-plan)
6. [Test Results Documentation](#6-test-results-documentation)
7. [Defect Management](#7-defect-management)

---

## 1. Overview

### 1.1 Testing Objectives

- Verify complete user workflows from start to finish
- Validate system performance under expected load
- Ensure user acceptance criteria are met
- Identify and document defects
- Verify system reliability and stability

### 1.2 Testing Scope

**In Scope:**
- All user workflows (login, transactions, inventory, employee management)
- API endpoint functionality
- Database operations
- Frontend-backend integration
- Performance under normal and peak load
- User acceptance scenarios

**Out of Scope:**
- Unit testing (covered separately)
- Security penetration testing (separate security audit)
- Browser compatibility (limited to modern browsers)

### 1.3 Testing Environment

**Test Environment Setup:**
- **Backend**: Django development server or production-like environment
- **Frontend**: React development build or production build
- **Database**: PostgreSQL 14+ (or SQLite for quick tests)
- **Browser**: Chrome, Firefox, Safari (latest versions)
- **Network**: Local or test network

**Test Data:**
- Pre-populated test database with:
  - 10+ employees (mix of Admin and Cashier)
  - 50+ inventory items
  - 20+ customers
  - 30+ historical transactions

---

## 2. End-to-End Testing

### 2.1 Test Scenarios Overview

End-to-end tests verify complete user workflows from start to finish, ensuring all system components work together correctly.

### 2.2 Test Scenario 1: Complete Sale Transaction Flow

**Objective:** Verify a complete sale transaction from login to receipt generation.

**Prerequisites:**
- System is running
- Test employee account exists (Cashier role)
- Inventory items available

**Test Steps:**

1. **Login**
   - Navigate to application URL
   - Enter valid Cashier credentials
   - Click "Login"
   - **Expected:** Redirected to Cashier dashboard

2. **Start New Sale**
   - Click "New Sale" button
   - **Expected:** Sale transaction interface opens

3. **Add Items**
   - Search for item by name or scan barcode
   - Add item to cart (quantity: 2)
   - Add another item (quantity: 1)
   - **Expected:** Items appear in cart with correct quantities and prices

4. **Apply Discount (Optional)**
   - Enter valid coupon code
   - Click "Apply Coupon"
   - **Expected:** Discount applied, total recalculated

5. **Review Transaction**
   - Verify subtotal, tax, and total
   - **Expected:** Calculations correct (subtotal + tax = total)

6. **Process Payment**
   - Select payment method (Cash)
   - Enter amount received
   - Click "Complete Transaction"
   - **Expected:** Transaction processed, receipt displayed

7. **Verify Transaction Saved**
   - Navigate to transaction history
   - Find the transaction
   - **Expected:** Transaction appears with correct details

8. **Verify Inventory Updated**
   - Navigate to inventory
   - Check item quantities
   - **Expected:** Quantities reduced by sold amounts

9. **Logout**
   - Click logout
   - **Expected:** Session cleared, redirected to login

**Test Data:**
- Employee: `cashier1` / `password123`
- Items: Item ID 1000 (quantity: 2), Item ID 1001 (quantity: 1)
- Coupon: `SAVE10` (10% discount)

**Expected Results:**
- ✅ All steps complete successfully
- ✅ Transaction saved to database
- ✅ Inventory updated correctly
- ✅ Receipt generated accurately
- ✅ Audit log entry created

**Actual Results:** [To be filled during testing]

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### 2.3 Test Scenario 2: Complete Rental Transaction Flow

**Objective:** Verify a complete rental transaction from customer lookup to rental record creation.

**Prerequisites:**
- System is running
- Test employee account exists (Cashier role)
- Rental items available in inventory

**Test Steps:**

1. **Login**
   - Navigate to application URL
   - Enter valid Cashier credentials
   - **Expected:** Redirected to Cashier dashboard

2. **Start New Rental**
   - Click "New Rental" button
   - **Expected:** Rental transaction interface opens

3. **Enter Customer Information**
   - Enter customer phone number: `6096515668`
   - Click "Lookup Customer"
   - **Expected:** Customer found or new customer created

4. **Add Rental Items**
   - Add rental item (quantity: 1)
   - Add another rental item (quantity: 2)
   - **Expected:** Items added with rental pricing

5. **Review Rental Details**
   - Verify rental period (default: 7 days)
   - Verify due date calculated correctly
   - Verify total amount
   - **Expected:** All details correct

6. **Process Rental**
   - Click "Complete Rental"
   - **Expected:** Rental transaction processed

7. **Verify Rental Records**
   - Navigate to rental management
   - Find rental records
   - **Expected:** Rental records created with correct due dates

8. **Verify Inventory Updated**
   - Check inventory quantities
   - **Expected:** Rental items quantity reduced

9. **Verify Customer Record**
   - Navigate to customer management
   - Find customer by phone number
   - **Expected:** Customer record shows active rentals

**Test Data:**
- Employee: `cashier1` / `password123`
- Customer Phone: `6096515668`
- Rental Items: Item ID 2000 (quantity: 1), Item ID 2001 (quantity: 2)
- Rental Period: 7 days

**Expected Results:**
- ✅ Rental transaction completed
- ✅ Rental records created with correct due dates
- ✅ Customer record updated
- ✅ Inventory quantities reduced
- ✅ Audit log entry created

**Actual Results:** [To be filled during testing]

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### 2.4 Test Scenario 3: Return Processing Flow

**Objective:** Verify return processing from rental lookup to inventory update.

**Prerequisites:**
- System is running
- Test employee account exists (Cashier role)
- Active rental exists in system

**Test Steps:**

1. **Login**
   - Navigate to application URL
   - Enter valid Cashier credentials
   - **Expected:** Redirected to Cashier dashboard

2. **Start Return Process**
   - Click "Process Return" button
   - **Expected:** Return interface opens

3. **Lookup Rental**
   - Enter customer phone number or rental ID
   - Click "Search"
   - **Expected:** Active rentals displayed

4. **Select Rental to Return**
   - Select rental item to return
   - **Expected:** Rental details displayed (due date, days overdue, etc.)

5. **Check Overdue Status**
   - Verify overdue calculation (if applicable)
   - **Expected:** Days overdue calculated correctly

6. **Process Return**
   - Click "Complete Return"
   - **Expected:** Return processed successfully

7. **Verify Rental Status Updated**
   - Check rental record
   - **Expected:** Rental marked as returned, return date set

8. **Verify Inventory Updated**
   - Check inventory quantities
   - **Expected:** Returned items added back to inventory

9. **Verify Overdue Fees (if applicable)**
   - Check transaction for overdue fees
   - **Expected:** Overdue fees calculated and charged correctly

**Test Data:**
- Employee: `cashier1` / `password123`
- Customer Phone: `6096515668`
- Rental ID: [From previous rental test]

**Expected Results:**
- ✅ Return processed successfully
- ✅ Rental status updated
- ✅ Inventory quantities increased
- ✅ Overdue fees calculated correctly (if applicable)
- ✅ Audit log entry created

**Actual Results:** [To be filled during testing]

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### 2.5 Test Scenario 4: Employee Management Flow (Admin)

**Objective:** Verify complete employee management workflow (Admin only).

**Prerequisites:**
- System is running
- Test employee account exists (Admin role)

**Test Steps:**

1. **Login as Admin**
   - Navigate to application URL
   - Enter valid Admin credentials
   - **Expected:** Redirected to Admin dashboard

2. **Navigate to Employee Management**
   - Click "Employee Management" menu
   - **Expected:** Employee list displayed

3. **View Employee Details**
   - Click on an employee
   - **Expected:** Employee details displayed

4. **Add New Employee**
   - Click "Add Employee" button
   - Fill in form:
     - Username: `newcashier`
     - Password: `newpass123`
     - First Name: `John`
     - Last Name: `Doe`
     - Position: `Cashier`
   - Click "Save"
   - **Expected:** Employee created, appears in list

5. **Verify New Employee Can Login**
   - Logout
   - Login with new employee credentials
   - **Expected:** Login successful, redirected to Cashier dashboard

6. **Update Employee**
   - Login as Admin
   - Navigate to employee management
   - Edit employee details
   - Update first name
   - Click "Save"
   - **Expected:** Changes saved, reflected in employee list

7. **Deactivate Employee**
   - Select employee
   - Click "Deactivate"
   - Confirm deactivation
   - **Expected:** Employee deactivated

8. **Verify Deactivated Employee Cannot Login**
   - Attempt login with deactivated employee
   - **Expected:** Login fails with appropriate message

**Test Data:**
- Admin: `admin1` / `adminpass123`
- New Employee: `newcashier` / `newpass123`

**Expected Results:**
- ✅ All CRUD operations work correctly
- ✅ New employee can login
- ✅ Updates persist
- ✅ Deactivated employee cannot login
- ✅ Audit log entries created for all actions

**Actual Results:** [To be filled during testing]

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### 2.6 Test Scenario 5: Inventory Management Flow

**Objective:** Verify inventory management operations.

**Prerequisites:**
- System is running
- Test employee account exists (Admin role)

**Test Steps:**

1. **Login as Admin**
   - Navigate to application URL
   - Enter valid Admin credentials
   - **Expected:** Redirected to Admin dashboard

2. **Navigate to Inventory**
   - Click "Inventory Management" menu
   - **Expected:** Inventory list displayed

3. **View Inventory Details**
   - Click on an item
   - **Expected:** Item details displayed (name, price, quantity, etc.)

4. **Update Item Quantity**
   - Select item
   - Click "Update Quantity"
   - Enter new quantity
   - Click "Save"
   - **Expected:** Quantity updated, reflected in list

5. **Update Item Price**
   - Select item
   - Click "Edit"
   - Update price
   - Click "Save"
   - **Expected:** Price updated

6. **Add New Item**
   - Click "Add Item" button
   - Fill in form:
     - Name: `Test Item`
     - Price: `19.99`
     - Quantity: `50`
   - Click "Save"
   - **Expected:** New item created, appears in list

7. **Verify Item in Transactions**
   - Create test sale transaction
   - Search for new item
   - **Expected:** New item appears in item selection

8. **Check Low Stock Alert (if implemented)**
   - Update item quantity to low value (e.g., 5)
   - **Expected:** Low stock alert displayed (if feature exists)

**Test Data:**
- Admin: `admin1` / `adminpass123`
- New Item: Name `Test Item`, Price `19.99`, Quantity `50`

**Expected Results:**
- ✅ All inventory operations work correctly
- ✅ Updates persist
- ✅ New items available in transactions
- ✅ Quantities accurate

**Actual Results:** [To be filled during testing]

**Status:** [ ] Pass [ ] Fail [ ] Blocked

---

### 2.7 Test Scenario 6: Error Handling and Edge Cases

**Objective:** Verify system handles errors and edge cases gracefully.

**Test Cases:**

#### 6.1 Invalid Login Attempts
- **Test:** Enter invalid username/password
- **Expected:** Error message displayed, login fails
- **Status:** [ ] Pass [ ] Fail

#### 6.2 Insufficient Inventory
- **Test:** Attempt to sell more items than available
- **Expected:** Error message, transaction prevented
- **Status:** [ ] Pass [ ] Fail

#### 6.3 Invalid Customer Phone
- **Test:** Enter invalid phone number format
- **Expected:** Validation error, transaction prevented
- **Status:** [ ] Pass [ ] Fail

#### 6.4 Expired Coupon
- **Test:** Apply expired coupon code
- **Expected:** Error message, coupon not applied
- **Status:** [ ] Pass [ ] Fail

#### 6.5 Network Interruption
- **Test:** Simulate network interruption during transaction
- **Expected:** Error handled gracefully, no data corruption
- **Status:** [ ] Pass [ ] Fail

#### 6.6 Concurrent Transactions
- **Test:** Multiple users process transactions simultaneously
- **Expected:** All transactions process correctly, no conflicts
- **Status:** [ ] Pass [ ] Fail

---

## 3. Performance Testing

### 3.1 Performance Testing Objectives

- Verify system performance under normal load
- Identify performance bottlenecks
- Validate response time requirements
- Test system under peak load conditions
- Verify database query performance

### 3.2 Performance Requirements

**Response Time Requirements:**
- API endpoints: < 200ms (average)
- Page load: < 2 seconds
- Transaction processing: < 1 second
- Database queries: < 100ms (average)

**Throughput Requirements:**
- Support 50+ concurrent users
- Process 100+ transactions per minute
- Handle 1000+ API requests per minute

### 3.3 Performance Test Scenarios

#### Test 1: API Endpoint Performance

**Objective:** Measure response times for all API endpoints.

**Tools:** Apache Bench (ab), curl, or Postman

**Test Commands:**

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test login endpoint
ab -n 100 -c 10 -p login.json -T application/json \
  http://localhost:8000/api/auth/login/

# Test inventory endpoint (requires authentication)
ab -n 100 -c 10 -H "Cookie: sessionid=<session-id>" \
  http://localhost:8000/api/inventory/

# Test transaction creation
ab -n 50 -c 5 -p transaction.json -T application/json \
  -H "Cookie: sessionid=<session-id>" \
  http://localhost:8000/api/transactions/
```

**Expected Results:**
- Average response time < 200ms
- 95th percentile < 500ms
- No errors

**Actual Results:**
- Average: [ ] ms
- 95th percentile: [ ] ms
- Errors: [ ] 

**Status:** [ ] Pass [ ] Fail

---

#### Test 2: Concurrent User Load Test

**Objective:** Test system under concurrent user load.

**Tools:** Locust, JMeter, or custom script

**Locust Test Script Example:**

```python
# locustfile.py
from locust import HttpUser, task, between

class POSUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/auth/login/", 
            json={"username": "cashier1", "password": "password123"})
        self.session_id = response.cookies.get('sessionid')
    
    @task(3)
    def view_inventory(self):
        self.client.get("/api/inventory/", 
            cookies={"sessionid": self.session_id})
    
    @task(2)
    def create_transaction(self):
        self.client.post("/api/transactions/",
            json={"transaction_type": "Sale", "items": [...]},
            cookies={"sessionid": self.session_id})
    
    @task(1)
    def view_transactions(self):
        self.client.get("/api/transactions/",
            cookies={"sessionid": self.session_id})
```

**Run Test:**
```bash
locust -f locustfile.py --host=http://localhost:8000
# Open browser to http://localhost:8089
# Set users: 50, spawn rate: 5
```

**Expected Results:**
- System handles 50 concurrent users
- Response times remain acceptable
- No errors or crashes
- Database connections stable

**Actual Results:**
- Max concurrent users: [ ]
- Average response time: [ ] ms
- Error rate: [ ]%
- Status: [ ] Pass [ ] Fail

---

#### Test 3: Database Query Performance

**Objective:** Verify database query performance.

**Tools:** Django database queries, PostgreSQL EXPLAIN ANALYZE

**Test Queries:**

```python
# Test inventory query
from django.test.utils import override_settings
from pos_app.models import Item
import time

start = time.time()
items = Item.objects.filter(is_active=True).select_related()
list(items)  # Force evaluation
duration = time.time() - start
print(f"Inventory query: {duration * 1000}ms")
```

**Expected Results:**
- Inventory query: < 50ms
- Transaction query: < 100ms
- Employee query: < 30ms

**Actual Results:**
- Inventory: [ ] ms
- Transactions: [ ] ms
- Employees: [ ] ms
- Status: [ ] Pass [ ] Fail

---

#### Test 4: Transaction Processing Throughput

**Objective:** Measure transaction processing throughput.

**Test Script:**

```python
import requests
import time
import concurrent.futures

def process_transaction(session):
    response = session.post("/api/transactions/",
        json={"transaction_type": "Sale", "items": [...]})
    return response.status_code == 201

# Test with 10 concurrent transactions
start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_transaction, session) 
               for _ in range(100)]
    results = [f.result() for f in futures]

duration = time.time() - start
throughput = 100 / duration
print(f"Throughput: {throughput} transactions/second")
```

**Expected Results:**
- Throughput: > 10 transactions/second
- All transactions successful
- No data corruption

**Actual Results:**
- Throughput: [ ] transactions/second
- Success rate: [ ]%
- Status: [ ] Pass [ ] Fail

---

### 3.4 Performance Test Results Summary

| Test Scenario | Target | Actual | Status |
|--------------|--------|--------|--------|
| API Response Time | < 200ms | [ ] ms | [ ] |
| Concurrent Users (50) | Stable | [ ] | [ ] |
| Database Queries | < 100ms | [ ] ms | [ ] |
| Transaction Throughput | > 10/sec | [ ] /sec | [ ] |
| Page Load Time | < 2s | [ ] s | [ ] |

---

## 4. User Acceptance Testing

### 4.1 UAT Overview

User Acceptance Testing (UAT) validates that the system meets business requirements and is acceptable to end users.

### 4.2 UAT Participants

- **Testers:** End users (Cashiers, Admins)
- **Facilitator:** QA Lead or Project Manager
- **Observer:** Development team member (for issue clarification)

### 4.3 UAT Scenarios

#### UAT Scenario 1: Cashier Daily Operations

**Objective:** Verify cashier can perform daily operations efficiently.

**Participants:** 2-3 Cashier users

**Test Steps:**

1. **Morning Setup**
   - Login to system
   - Verify dashboard displays correctly
   - Check inventory levels
   - Review pending rentals

2. **Process Sales**
   - Process 10 sale transactions
   - Mix of cash and card payments
   - Apply discounts where applicable
   - Generate receipts

3. **Process Rentals**
   - Create 5 rental transactions
   - Different customers
   - Various rental items

4. **Process Returns**
   - Process 3 returns
   - Verify overdue calculations
   - Update inventory

5. **End of Day**
   - Review transaction summary
   - Generate daily report
   - Logout

**Acceptance Criteria:**
- [ ] All operations completed without errors
- [ ] System is intuitive and easy to use
- [ ] Response times acceptable
- [ ] All data accurate

**User Feedback:**
- Ease of use: [ ] Excellent [ ] Good [ ] Fair [ ] Poor
- Performance: [ ] Excellent [ ] Good [ ] Fair [ ] Poor
- Overall satisfaction: [ ] Excellent [ ] Good [ ] Fair [ ] Poor

**Comments:**
[User feedback and comments]

**Status:** [ ] Accepted [ ] Needs Changes [ ] Rejected

---

#### UAT Scenario 2: Admin Management Tasks

**Objective:** Verify admin can manage system effectively.

**Participants:** 1-2 Admin users

**Test Steps:**

1. **Employee Management**
   - Add 2 new employees
   - Update employee information
   - Deactivate 1 employee
   - Verify permissions

2. **Inventory Management**
   - Add 5 new items
   - Update item prices
   - Adjust quantities
   - Set low stock alerts

3. **Reports and Analytics**
   - Generate sales report
   - Generate rental report
   - View transaction history
   - Export data

4. **System Configuration**
   - Update tax rates
   - Configure discount rules
   - Set rental periods

**Acceptance Criteria:**
- [ ] All management tasks completed successfully
- [ ] Reports accurate and useful
- [ ] Configuration changes persist
- [ ] System stable after changes

**User Feedback:**
- Functionality: [ ] Excellent [ ] Good [ ] Fair [ ] Poor
- Reports quality: [ ] Excellent [ ] Good [ ] Fair [ ] Poor
- Overall satisfaction: [ ] Excellent [ ] Good [ ] Fair [ ] Poor

**Comments:**
[User feedback and comments]

**Status:** [ ] Accepted [ ] Needs Changes [ ] Rejected

---

#### UAT Scenario 3: System Usability

**Objective:** Evaluate overall system usability.

**Participants:** All user roles

**Evaluation Areas:**

1. **User Interface**
   - [ ] Intuitive navigation
   - [ ] Clear labels and instructions
   - [ ] Consistent design
   - [ ] Responsive layout

2. **Error Handling**
   - [ ] Clear error messages
   - [ ] Helpful guidance
   - [ ] Recovery options

3. **Performance**
   - [ ] Fast response times
   - [ ] No lag or delays
   - [ ] Smooth interactions

4. **Documentation**
   - [ ] Help documentation available
   - [ ] Clear instructions
   - [ ] Examples provided

**User Ratings (1-5 scale):**
- Interface Design: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Ease of Use: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Performance: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
- Overall: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5

**Status:** [ ] Accepted [ ] Needs Changes [ ] Rejected

---

### 4.4 UAT Sign-Off

**Test Completion Date:** [Date]

**Participants:**
- Cashier 1: _________________ Date: _______
- Cashier 2: _________________ Date: _______
- Admin 1: _________________ Date: _______

**Overall UAT Status:** [ ] Accepted [ ] Conditionally Accepted [ ] Rejected

**Conditions (if applicable):**
[List any conditions or required changes]

**Sign-Off:**
- Project Manager: _________________ Date: _______
- Lead Developer: _________________ Date: _______

---

## 5. Test Execution Plan

### 5.1 Test Schedule

| Phase | Duration | Activities |
|-------|----------|------------|
| **Preparation** | 2 days | Test environment setup, test data preparation |
| **E2E Testing** | 3 days | Execute all end-to-end test scenarios |
| **Performance Testing** | 2 days | Execute performance test scenarios |
| **UAT** | 3 days | User acceptance testing sessions |
| **Defect Resolution** | 3 days | Fix defects, retest |
| **Final Verification** | 1 day | Final test execution, sign-off |

**Total Duration:** 14 days

### 5.2 Test Execution Order

1. **Day 1-2:** Setup and preparation
2. **Day 3:** E2E Test Scenarios 1-3 (Transactions)
3. **Day 4:** E2E Test Scenarios 4-6 (Management)
4. **Day 5:** Error handling and edge cases
5. **Day 6-7:** Performance testing
6. **Day 8-10:** User acceptance testing
7. **Day 11-13:** Defect resolution and retesting
8. **Day 14:** Final verification and sign-off

### 5.3 Test Execution Guidelines

**Before Testing:**
- Verify test environment is ready
- Ensure test data is loaded
- Confirm all prerequisites are met
- Review test scenarios

**During Testing:**
- Execute tests in order
- Document actual results
- Capture screenshots for defects
- Note any deviations from expected behavior

**After Testing:**
- Document all results
- Report defects immediately
- Update test status
- Prepare test summary report

---

## 6. Test Results Documentation

### 6.1 Test Summary Report

**Test Execution Date:** [Date]
**Test Environment:** [Environment details]
**Tester:** [Tester name]

**Summary Statistics:**
- Total Test Scenarios: 6
- Passed: [ ]
- Failed: [ ]
- Blocked: [ ]
- Not Executed: [ ]

**Pass Rate:** [ ]%

### 6.2 Detailed Test Results

[Include detailed results for each test scenario]

### 6.3 Defect Summary

**Total Defects Found:** [ ]
**Critical:** [ ]
**High:** [ ]
**Medium:** [ ]
**Low:** [ ]

**Defect Breakdown:**
- Functional: [ ]
- Performance: [ ]
- Usability: [ ]
- Integration: [ ]

---

## 7. Defect Management

### 7.1 Defect Reporting Template

**Defect ID:** [DEF-001]
**Title:** [Brief description]
**Severity:** [ ] Critical [ ] High [ ] Medium [ ] Low
**Priority:** [ ] P1 [ ] P2 [ ] P3 [ ] P4

**Description:**
[Detailed description of the defect]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happens]

**Environment:**
- Browser: [ ]
- OS: [ ]
- Version: [ ]

**Screenshots/Logs:**
[Attach relevant files]

**Status:** [ ] New [ ] Assigned [ ] In Progress [ ] Fixed [ ] Verified [ ] Closed

**Assigned To:** [Developer name]
**Reported By:** [Tester name]
**Date Reported:** [Date]
**Date Fixed:** [Date]

### 7.2 Defect Severity Levels

**Critical:**
- System crash or data loss
- Security vulnerability
- Complete feature failure

**High:**
- Major feature malfunction
- Significant performance issue
- Data integrity issue

**Medium:**
- Minor feature issue
- Workaround available
- Moderate performance impact

**Low:**
- Cosmetic issue
- Minor usability issue
- Documentation error

---

## Appendix A: Test Data

### A.1 Test Employees

| Username | Password | Role | Status |
|----------|----------|------|--------|
| admin1 | adminpass123 | Admin | Active |
| cashier1 | password123 | Cashier | Active |
| cashier2 | password123 | Cashier | Active |

### A.2 Test Items

| Item ID | Name | Price | Quantity |
|---------|------|-------|----------|
| 1000 | Test Item 1 | 10.00 | 100 |
| 1001 | Test Item 2 | 25.50 | 50 |
| 2000 | Rental Item 1 | 5.00 | 20 |

### A.3 Test Customers

| Phone Number | Name | Status |
|--------------|------|--------|
| 6096515668 | Test Customer 1 | Active |
| 5551234567 | Test Customer 2 | Active |

---

**Document Version:** 1.0  
**Last Updated:** [Current Date]  
**Prepared By:** QA Team  
**Approved By:** [Project Manager]

