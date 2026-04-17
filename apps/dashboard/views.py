from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.job_applications.models import Application
from apps.jobs.models import Job
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def dashboard_home(request):
    user = request.user
    
    if user.is_staff:
        return redirect('admin-dashboard')
    
    if user.role == 'employer':
        return redirect('employer-deshboard')
    
    return redirect('jobseeker-dashboard')

@login_required
def jobseeker_dashboard(request):
    applications = (
        Application.objects
        .filter(user=request.user)
        .select_related('job')
        .order_by('applied_at')
    )

    context = {
        'applications': applications,
        'applications_count': applications.count()
    }

    return render(request, 'dashboard/jobseeker_dashboard.html', context)

@login_required
def employer_dashboard(request):
    jobs = (
        Job.objects
        .filter(posted_by=request.user)
        .order_by('posted_at')
    )

    context = {
        'jobs': jobs,
        'jobs_count': jobs.count(),
    }
    return render(request, 'dashboard/employer_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    context = {
        'users_count': User.objects.count(),
        'jobs_count': Job.objects.count(),
        'applications_count': Application.objects.count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
