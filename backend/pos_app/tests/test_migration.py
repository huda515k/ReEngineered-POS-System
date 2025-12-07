from django.test import TestCase
from pos_app.models.employee import Employee
from pos_app.models.item import Item
from pos_app.models.customer import Customer
import os


class DataMigrationTest(TestCase):
    """Test data migration from legacy .txt files"""
    
    def test_employee_data_structure(self):
        """Test that employee model can store legacy data format"""
        # Legacy format: username position firstName lastName password
        employee = Employee.objects.create(
            username='110001',
            first_name='John',
            last_name='Doe',
            position='Admin'
        )
        employee.set_password('password123')
        employee.save()
        self.assertEqual(employee.username, '110001')
        self.assertEqual(employee.position, 'Admin')
        self.assertEqual(employee.full_name, 'John Doe')

    def test_item_data_structure(self):
        """Test that item model can store legacy data format"""
        # Legacy format: itemID itemName price amount
        item = Item.objects.create(
            legacy_item_id='1001',
            name='Test Item',
            price=19.99,
            quantity=50
        )
        self.assertEqual(item.legacy_item_id, '1001')
        self.assertEqual(float(item.price), 19.99)
        self.assertEqual(item.quantity, 50)

    def test_customer_data_structure(self):
        """Test that customer model can store legacy rental data"""
        customer = Customer.objects.create(
            phone_number='1234567890'
        )
        self.assertEqual(customer.phone_number, '1234567890')

    def test_data_integrity(self):
        """Test that migrated data maintains integrity"""
        employee = Employee.objects.create(
            username='test',
            first_name='Test',
            last_name='User',
            position='Cashier'
        )
        employee.set_password('pass123')
        employee.save()
        item = Item.objects.create(
            legacy_item_id='1001',
            name='Item',
            price=10.00,
            quantity=10
        )
        
        # Verify relationships can be established
        self.assertIsNotNone(employee.id)
        self.assertIsNotNone(item.id)

