from django.urls import path
from .views import (
    dashboard_home,
    jobseeker_dashboard,
    employer_dashboard,
    admin_dashboard
)

urlpatterns = [
    path('', dashboard_home, name='dashboard'),
    path('jobseeker/', jobseeker_dashboard, name='jobseeker-dashboard'),
    path('employer', employer_dashboard, name='employer-dashboard'),
    path('admin/', admin_dashboard, name='admin-dashboard'),
]
