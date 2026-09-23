from decimal import Decimal

from django.db import migrations


def seed_demo_jobs(apps, schema_editor):
    # Use the historical model provided by Django migrations.
    Job = apps.get_model("jobs", "Job")
    database = schema_editor.connection.alias

    jobs = [
        {
            "slug": "demo-django-developer",
            "title": "Django Developer (Demo)",
            "company_name": "Example Software Company",
            "location": "Nairobi",
            "employment_type": "FT",
            "category": "Software Development",
            "description": (
                "Sample listing for local testing. "
                "Build and maintain Django web applications."
            ),
            "requirements": "Python, Django, PostgreSQL and Git.",
            "salary_min": Decimal("80000.00"),
            "salary_max": Decimal("120000.00"),
            "is_featured": True,
        },
        {
            "slug": "demo-devops-engineer",
            "title": "DevOps Engineer (Demo)",
            "company_name": "Example Cloud Company",
            "location": "Remote",
            "employment_type": "CT",
            "category": "DevOps",
            "description": (
                "Sample listing for local testing. "
                "Manage CI/CD pipelines and container deployments."
            ),
            "requirements": "Linux, Docker, Jenkins and networking.",
            "salary_min": Decimal("100000.00"),
            "salary_max": Decimal("160000.00"),
            "is_featured": True,
        },
        {
            "slug": "demo-ict-intern",
            "title": "ICT Intern (Demo)",
            "company_name": "Example Support Company",
            "location": "Narok",
            "employment_type": "IN",
            "category": "ICT Support",
            "description": (
                "Sample listing for local testing. "
                "Assist with user support and equipment maintenance."
            ),
            "requirements": "Basic troubleshooting and communication skills.",
            "salary_min": Decimal("15000.00"),
            "salary_max": Decimal("25000.00"),
            "is_featured": False,
        },
    ]

    for job in jobs:
        slug = job.pop("slug")

        # Explicit slugs are needed because historical models
        # do not include your custom save() implementation.
        Job.objects.using(database).get_or_create(
            slug=slug,
            defaults={
                **job,
                "is_active": True,
                "application_deadline": None,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_demo_jobs,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
