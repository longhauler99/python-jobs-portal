from django.shortcuts import render
from apps.jobs.models import Job

# Create your views here.
def home(request):
    return render(request, 'home.html')
