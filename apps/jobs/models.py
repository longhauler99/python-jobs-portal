from django.db import models
from django.utils.text import slugify

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
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
    is_featured = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.company_name}"

    def salary_range(self):
        return f"{self.salary_min:,} - {self.salary_max:,}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.company_name}")
            slug = base_slug
            counter = 1

            # Ensure uniqueness
            while Job.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
