from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CandidateProfile, EmployerProfile

# apps/profiles/views.py
@login_required
def profile_detail_view(request):
    # Safe retrieval based on user types
    if request.user.role == 'job_seeker':
        profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    elif request.user.role == 'employer':
        profile, created = EmployerProfile.objects.get_or_create(user=request.user)
    else:
        profile = None

    context = {
        'profile': profile
    }
    return render(request, 'profiles/profile_detail.html', context)

@login_required
def edit_candidate_profile(request):
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    # if getattr(request.user, 'role', None) != 'job_seeker':
    #     return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Update User Model Names
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        # Update Profile Model Fields
        profile.id_number = request.POST.get('id_number', '').strip()
        profile.phone_number = request.POST.get('phone_number', '').strip()
        profile.skills = request.POST.get('skills', '').strip()
        profile.experience = request.POST.get('experience', '').strip()
        profile.availability = request.POST.get('availability') == 'on'

        if request.FILES.get('resume'):
            profile.resume = request.FILES['resume']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile_detail')

    return render(request, 'profiles/edit_candidate_profile.html')
