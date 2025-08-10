import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('normal', 'Normal User'),
        ('hirer', 'Hirer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username