from django.urls import path
from .views import (
    LoginView, LogoutView,
    EmployeeListView, EmployeeDetailView,
    ItemListView, ItemDetailView,
    TransactionListView, TransactionDetailView,
    CreateSaleView, CreateRentalView, ProcessReturnView,
    GetOutstandingRentalsView
)
from .views.api_root_view import api_root

app_name = 'pos_app'

urlpatterns = [
    # API root - shows available endpoints
    path('', api_root, name='api-root'),
    
    # Authentication
    path('auth/login/', LoginView, name='login'),
    path('auth/logout/', LogoutView, name='logout'),
    
    # Employees
    path('employees/', EmployeeListView, name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView, name='employee-detail'),
    
    # Items
    path('items/', ItemListView, name='item-list'),
    path('items/<int:pk>/', ItemDetailView, name='item-detail'),
    
    # Transactions
    path('transactions/', TransactionListView, name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView, name='transaction-detail'),
    path('transactions/sale/', CreateSaleView, name='create-sale'),
    path('transactions/rental/', CreateRentalView, name='create-rental'),
    path('transactions/return/', ProcessReturnView, name='process-return'),
    path('transactions/outstanding-rentals/', GetOutstandingRentalsView, name='get-outstanding-rentals'),
]

