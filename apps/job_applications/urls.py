# apps/applications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('apply/<slug:slug>/', views.apply_job, name='apply-job'),
]