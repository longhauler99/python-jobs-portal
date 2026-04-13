from django.db import models
from django.contrib.auth.models import User
from apps.jobs.models import Job

# Create your models here.
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')

    status = models.CharField(max_length=50,
              choices=([
                  ('pending', 'Pending'),
                  ('reviewed', 'Reviewed'),
                  ('accepted', 'Accepted'),
                  ('rejected', 'Rejected'),
              ]
          ),
          default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (('user', 'job'),)    # prevents duplicate applications

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title}"
