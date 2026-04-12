from os import name

from django.shortcuts import render
from apps.jobs.models import Job

# Create your views here.
def index(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs/index.html', context)

def job_detail(request, job_id):
    job = Job.objects.get(pk=job_id)
    context = {'job': job}
    return render(request, 'jobs/job_details.html', context)
