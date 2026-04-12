from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('FT', 'Full Time'),
            ('PT', 'Part Time'),
            ('CT', 'Contract'),
            ('IN', 'Internship'),
        ]
    )
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}, {self.company_name}, {self.salary_min}, {self.salary_max}, {self.employment_type}"

