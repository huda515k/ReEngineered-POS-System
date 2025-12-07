"""
Employee Service - Business logic for employee operations
"""
from ..models import Employee, AuditLog


class EmployeeService:
    """Service class for handling employee operations"""
    
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate employee
        
        Returns:
            Employee object if authenticated, None otherwise
        """
        try:
            employee = Employee.objects.get(username=username, is_active=True)
            if employee.check_password(password):
                # Log successful login
                AuditLog.objects.create(
                    employee=employee,
                    action='login',
                    details=f"Employee {username} logged in"
                )
                return employee
        except Employee.DoesNotExist:
            pass
        return None
    
    @staticmethod
    def logout(employee_id):
        """Log employee logout"""
        try:
            employee = Employee.objects.get(id=employee_id)
            AuditLog.objects.create(
                employee=employee,
                action='logout',
                details=f"Employee {employee.username} logged out"
            )
        except Employee.DoesNotExist:
            pass
    
    @staticmethod
    def create_employee(username, password, first_name, last_name, position):
        """Create a new employee"""
        employee = Employee(
            username=username,
            first_name=first_name,
            last_name=last_name,
            position=position
        )
        employee.set_password(password)
        employee.save()
        
        # Log employee creation
        AuditLog.objects.create(
            employee=employee,
            action='employee_created',
            details=f"New employee {username} created"
        )
        
        return employee
    
    @staticmethod
    def update_employee(employee_id, **kwargs):
        """Update employee information"""
        employee = Employee.objects.get(id=employee_id)
        
        if 'password' in kwargs:
            employee.set_password(kwargs.pop('password'))
        
        for key, value in kwargs.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        
        employee.save()
        
        # Log employee update
        AuditLog.objects.create(
            employee=employee,
            action='employee_updated',
            details=f"Employee {employee.username} updated"
        )
        
        return employee
    
    @staticmethod
    def delete_employee(employee_id):
        """Soft delete employee (set is_active=False)"""
        employee = Employee.objects.get(id=employee_id)
        employee.is_active = False
        employee.save()
        
        # Log employee deletion
        AuditLog.objects.create(
            employee=employee,
            action='employee_deleted',
            details=f"Employee {employee.username} deactivated"
        )
        
        return employee
    
    @staticmethod
    def get_all_employees():
        """Get all active employees"""
        return Employee.objects.filter(is_active=True)
    
    @staticmethod
    def get_employee_by_id(employee_id):
        """Get employee by ID"""
        return Employee.objects.get(id=employee_id)

