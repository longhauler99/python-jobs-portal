from django.shortcuts import render
from apps.listings.models import Job

# Create your views here.
def index(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'listings/index.html', context)
