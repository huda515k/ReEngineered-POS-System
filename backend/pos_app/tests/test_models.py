from django.test import TestCase
from django.core.exceptions import ValidationError
from pos_app.models.employee import Employee
from pos_app.models.item import Item
from pos_app.models.customer import Customer
from pos_app.models.transaction import Transaction
from pos_app.models.coupon import Coupon


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            position='Cashier'
        )
        self.employee.set_password('testpass123')
        self.employee.save()

    def test_employee_creation(self):
        self.assertEqual(self.employee.username, 'testuser')
        self.assertEqual(self.employee.full_name, 'Test User')
        self.assertTrue(self.employee.is_active)

    def test_employee_password_hashing(self):
        self.assertNotEqual(self.employee.password_hash, 'testpass123')
        self.assertTrue(self.employee.check_password('testpass123'))

    def test_employee_str_representation(self):
        self.assertIn('testuser', str(self.employee))


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            legacy_item_id='1001',
            name='Test Item',
            price=19.99,
            quantity=50
        )

    def test_item_creation(self):
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(float(self.item.price), 19.99)
        self.assertEqual(self.item.quantity, 50)

    def test_item_str_representation(self):
        self.assertIn('Test Item', str(self.item))


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            phone_number='1234567890'
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.phone_number, '1234567890')

    def test_customer_str_representation(self):
        self.assertIn('1234567890', str(self.customer))


class TransactionModelTest(TestCase):
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
        self.transaction = Transaction.objects.create(
            employee=self.employee,
            transaction_type='Sale',
            total_amount=10.60  # $10 + 6% tax
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.transaction_type, 'Sale')
        self.assertEqual(float(self.transaction.total_amount), 10.60)
        self.assertEqual(self.transaction.employee, self.employee)


class CouponModelTest(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='TEST10',
            discount_percentage=10.0,
            is_active=True
        )

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.code, 'TEST10')
        self.assertEqual(float(self.coupon.discount_percentage), 10.0)
        self.assertTrue(self.coupon.is_active)

