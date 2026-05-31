from django.db import models
from django.conf import settings

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    id_number = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    availability = models.BooleanField(default=True, help_text='Designates if the candidate is looking for work.')

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f"Candidate: {self.user.email}"

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')

    company_name = models.CharField(max_length=255, blank=True)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)

    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, help_text='e.g., Nairobi, Kenya')
    industry = models.CharField(max_length=100, blank=True, help_text='e.g., Technology, Healthcare')

    is_verified = models.BooleanField(default=False, help_text="Admin check to verify authentic employers")

    def __str__(self):
        return f"Employer: {self.company_name or self.user.email}"

