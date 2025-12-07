"""
URL configuration for POS System project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from pos_app.views.api_root_view import api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    # Redirect /api to /api/ (with trailing slash)
    path('api', RedirectView.as_view(url='/api/', permanent=False), name='api-redirect'),
    path('api/', include('pos_app.urls')),
]

