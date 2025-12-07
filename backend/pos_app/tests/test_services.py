from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from pos_app.models.employee import Employee
from pos_app.models.item import Item
from pos_app.models.customer import Customer
from pos_app.models.transaction import Transaction
from pos_app.models.rental import Rental
from pos_app.services.employee_service import EmployeeService
from pos_app.services.inventory_service import InventoryService
from pos_app.services.transaction_service import TransactionService
from pos_app.services.rental_service import RentalService


class EmployeeServiceTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            position='Cashier'
        )
        self.employee.set_password('testpass123')
        self.employee.save()

    def test_authenticate_success(self):
        employee = EmployeeService.authenticate('testuser', 'testpass123')
        self.assertIsNotNone(employee)
        self.assertEqual(employee.username, 'testuser')

    def test_authenticate_failure_wrong_password(self):
        employee = EmployeeService.authenticate('testuser', 'wrongpass')
        self.assertIsNone(employee)

    def test_authenticate_failure_wrong_username(self):
        employee = EmployeeService.authenticate('wronguser', 'testpass123')
        self.assertIsNone(employee)


class InventoryServiceTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            legacy_item_id='1001',
            name='Test Item',
            price=19.99,
            quantity=50
        )

    def test_get_item_by_id(self):
        item = InventoryService.get_item_by_id(self.item.id)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, 'Test Item')

    def test_update_item_quantity(self):
        InventoryService.update_item_quantity(self.item.id, 45)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 45)

    def test_search_items(self):
        items = InventoryService.search_items('Test')
        self.assertGreater(len(items), 0)
        self.assertEqual(items[0].name, 'Test Item')


class TransactionServiceTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            username='cashier1',
            first_name='Cashier',
            last_name='One',
            position='Cashier'
        )
        self.employee.set_password('pass123')
        self.employee.save()
        self.item = Item.objects.create(
            legacy_item_id='1001',
            name='Test Item',
            price=10.00,
            quantity=10
        )

    def test_create_sale_transaction(self):
        items_data = [{'item_id': self.item.id, 'quantity': 2}]
        transaction = TransactionService.create_sale(
            employee_id=self.employee.id,
            items_data=items_data
        )
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_type, 'Sale')
        # 2 * $10 = $20, + 6% tax = $21.20
        self.assertAlmostEqual(float(transaction.total_amount), 21.20, places=2)

    def test_create_sale_updates_inventory(self):
        initial_quantity = self.item.quantity
        items_data = [{'item_id': self.item.id, 'quantity': 2}]
        TransactionService.create_sale(
            employee_id=self.employee.id,
            items_data=items_data
        )
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, initial_quantity - 2)

    def test_create_rental_transaction(self):
        customer = Customer.objects.create(phone_number='1234567890')
        items_data = [{'item_id': self.item.id, 'quantity': 2}]
        transaction = TransactionService.create_rental(
            employee_id=self.employee.id,
            customer_phone='1234567890',
            items_data=items_data
        )
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_type, 'Rental')
        # 2 * $10 = $20, + 6% tax = $21.20
        self.assertAlmostEqual(float(transaction.total_amount), 21.20, places=2)

    def test_create_rental_creates_rental_records(self):
        customer = Customer.objects.create(phone_number='1234567890')
        items_data = [{'item_id': self.item.id, 'quantity': 2}]
        transaction = TransactionService.create_rental(
            employee_id=self.employee.id,
            customer_phone='1234567890',
            items_data=items_data
        )
        rentals = Rental.objects.filter(transaction=transaction)
        self.assertEqual(rentals.count(), 2)  # 2 items rented

    def test_process_return(self):
        customer = Customer.objects.create(phone_number='1234567890')
        items_data = [{'item_id': self.item.id, 'quantity': 2}]
        transaction = TransactionService.create_rental(
            employee_id=self.employee.id,
            customer_phone='1234567890',
            items_data=items_data
        )
        # After rental, quantity should be reduced
        self.item.refresh_from_db()
        quantity_after_rental = self.item.quantity
        
        rentals = Rental.objects.filter(transaction=transaction)
        item_ids = [rental.item.id for rental in rentals]
        
        returned = TransactionService.process_return('1234567890', item_ids)
        self.assertEqual(len(returned), 2)
        self.assertTrue(all(r.is_returned for r in returned))
        
        # After return, quantity should be restored
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, quantity_after_rental + 2)


class RentalServiceTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(phone_number='1234567890')
        self.item = Item.objects.create(
            legacy_item_id='1001',
            name='Test Item',
            price=10.00,
            quantity=10
        )
        self.employee = Employee.objects.create(
            username='cashier1',
            first_name='Cashier',
            last_name='One',
            position='Cashier'
        )
        self.employee.set_password('pass123')
        self.employee.save()

    def test_get_active_rentals(self):
        # Create a rental transaction
        items_data = [{'item_id': self.item.id, 'quantity': 1}]
        TransactionService.create_rental(
            employee_id=self.employee.id,
            customer_phone='1234567890',
            items_data=items_data
        )
        
        active_rentals = RentalService.get_active_rentals('1234567890')
        self.assertEqual(active_rentals.count(), 1)
        self.assertFalse(active_rentals.first().is_returned)

    def test_get_customer_rentals(self):
        items_data = [{'item_id': self.item.id, 'quantity': 1}]
        TransactionService.create_rental(
            employee_id=self.employee.id,
            customer_phone='1234567890',
            items_data=items_data
        )
        
        rentals = RentalService.get_customer_rentals('1234567890')
        self.assertGreaterEqual(rentals.count(), 1)

    def test_check_customer_has_outstanding_returns(self):
        items_data = [{'item_id': self.item.id, 'quantity': 1}]
        TransactionService.create_rental(
            employee_id=self.employee.id,
            customer_phone='1234567890',
            items_data=items_data
        )
        
        has_outstanding = RentalService.check_customer_has_outstanding_returns('1234567890')
        self.assertTrue(has_outstanding)

