from os import name
from django.shortcuts import render, get_object_or_404
from apps.jobs.models import Job

# Create your views here.
def index(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs/index.html', context)

def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    return render(request, 'jobs/job_details.html', {'job': job})
