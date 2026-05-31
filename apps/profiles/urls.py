# apps/applications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_detail_view, name='profile_detail'),
    path('candidate/edit/', views.edit_candidate_profile, name='edit_candidate_profile'),
]