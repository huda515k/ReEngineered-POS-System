"""
Custom permissions for POS system
"""
from rest_framework import permissions


class IsEmployeeAuthenticated(permissions.BasePermission):
    """
    Custom permission to check if employee is authenticated via session
    """
    def has_permission(self, request, view):
        # Check if employee_id exists in session
        return bool(request.session.get('employee_id'))

