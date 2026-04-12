from django.urls import path
from . import views

# Define a list of URL patterns
urlpatterns = [
    path('jobs/', views.index, name='jobs'),
    path('jobs-details/<slug:slug>', views.job_detail, name='job-details'),
]