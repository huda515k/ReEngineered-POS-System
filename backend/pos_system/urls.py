"""
URL configuration for POS System project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint with available endpoints"""
    return JsonResponse({
        'message': 'POS System API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
            },
            'employees': {
                'list': '/api/employees/',
                'detail': '/api/employees/{id}/',
            },
            'items': {
                'list': '/api/items/',
                'detail': '/api/items/{id}/',
                'search': '/api/items/?search=query',
            },
            'transactions': {
                'list': '/api/transactions/',
                'detail': '/api/transactions/{id}/',
                'create_sale': '/api/transactions/sale/',
                'create_rental': '/api/transactions/rental/',
                'process_return': '/api/transactions/return/',
            },
            'admin': '/admin/',
        },
        'documentation': 'See README.md for API documentation'
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('pos_app.urls')),
]

