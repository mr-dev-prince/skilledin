from django.db import models
from django.conf import settings
import uuid

class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full-Time'),
        ('internship', 'Internship'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255, help_text="Comma-separated tech skills")
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
    poster = models.URLField(blank=True, null=True, help_text="URL to the poster image of the job")
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')


    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.URLField(blank=True, null=True, help_text="URL to the applicant's resume")
    notice_period = models.CharField(max_length=50, blank=True, null=True, help_text="Notice period of the applicant")
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Expected salary of the applicant")
    message = models.TextField(blank=True, null=True, help_text="Additional message from the applicant")

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"