from rest_framework import serializers
from ..models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'position', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class EmployeeLoginSerializer(serializers.Serializer):
    """Serializer for employee login"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255, write_only=True)
    
    def validate(self, data):
        """Validate login credentials"""
        from ..services import EmployeeService
        
        employee = EmployeeService.authenticate(
            data['username'],
            data['password']
        )
        
        if not employee:
            raise serializers.ValidationError("Invalid username or password")
        
        data['employee'] = employee
        return data


class CreateEmployeeSerializer(serializers.ModelSerializer):
    """Serializer for creating employees"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Employee
        fields = ['username', 'password', 'first_name', 'last_name', 'position']
    
    def create(self, validated_data):
        """Create employee with hashed password"""
        from ..services import EmployeeService
        
        password = validated_data.pop('password')
        employee = EmployeeService.create_employee(
            password=password,
            **validated_data
        )
        return employee

