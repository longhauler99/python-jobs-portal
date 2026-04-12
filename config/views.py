from django.shortcuts import render
from apps.jobs.models import Job

# Create your views here.
def home(request):
    featured_jobs = Job.objects.filter(is_featured=True)[:3]
    context = {'featured_jobs': featured_jobs}
    return render(request, 'home.html', context)
