from django.urls import path
from . import views

# Define a list of URL patterns
urlpatterns = [
    path('jobs/', views.index, name='jobs'),
    path('jobs-details/<int:job_id>', views.job_detail, name='job-details'),
]