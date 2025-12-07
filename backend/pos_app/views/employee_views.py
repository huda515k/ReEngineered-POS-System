from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..serializers import EmployeeSerializer, CreateEmployeeSerializer
from ..services import EmployeeService
from ..models import Employee
from ..permissions import IsEmployeeAuthenticated


@api_view(['GET', 'POST'])
@permission_classes([IsEmployeeAuthenticated])
def EmployeeListView(request):
    """List all employees or create a new employee"""
    
    # Only admins can manage employees
    employee_id = request.session.get('employee_id')
    if employee_id:
        employee = Employee.objects.get(id=employee_id)
        if not employee.is_admin():
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    if request.method == 'GET':
        employees = EmployeeService.get_all_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                EmployeeSerializer(employee).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsEmployeeAuthenticated])
def EmployeeDetailView(request, pk):
    """Retrieve, update, or delete an employee"""
    
    # Only admins can manage employees
    employee_id = request.session.get('employee_id')
    if employee_id:
        employee = Employee.objects.get(id=employee_id)
        if not employee.is_admin():
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    try:
        employee = EmployeeService.get_employee_by_id(pk)
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            updated_employee = EmployeeService.update_employee(pk, **serializer.validated_data)
            return Response(EmployeeSerializer(updated_employee).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        EmployeeService.delete_employee(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

