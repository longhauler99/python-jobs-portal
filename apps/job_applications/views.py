from django.shortcuts import render

# Create your views here.
# apps/applications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.jobs.models import Job
from .models import Application

@login_required
def apply_job(request, slug):
    job = get_object_or_404(Job, slug=slug)

    # prevent duplicate applications
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You already applied for this job.")
        return redirect('job-details', slug=slug)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')

        Application.objects.create(
            user=request.user,
            job=job,
            cover_letter=cover_letter,
            resume=resume
        )

        messages.success(request, "Application submitted successfully!")
        return redirect('job-details', slug=slug)

    return render(request, 'job_applications/apply.html', {'job': job})