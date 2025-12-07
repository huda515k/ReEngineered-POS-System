from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..serializers import EmployeeLoginSerializer, EmployeeSerializer
from ..services import EmployeeService
from ..permissions import IsEmployeeAuthenticated


@api_view(['POST'])
@permission_classes([AllowAny])
def LoginView(request):
    """Employee login endpoint"""
    serializer = EmployeeLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        employee = serializer.validated_data['employee']
        # Store employee ID in session
        request.session['employee_id'] = employee.id
        request.session['employee_position'] = employee.position
        
        return Response({
            'message': 'Login successful',
            'employee': EmployeeSerializer(employee).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsEmployeeAuthenticated])
def LogoutView(request):
    """Employee logout endpoint"""
    employee_id = request.session.get('employee_id')
    
    if employee_id:
        EmployeeService.logout(employee_id)
        request.session.flush()
    
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

