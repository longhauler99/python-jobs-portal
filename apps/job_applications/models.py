from django.db import models
# from django.contrib.auth import get_user_model
from apps.jobs.models import Job
from django.conf import settings

# User = get_user_model()
class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
