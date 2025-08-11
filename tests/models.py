import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Test(models.Model):
    EVALUATION_TYPE_CHOICES = [
        ('auto', 'Automatic'),
        ('manual', 'Manual'),
    ]
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private (Invite Only)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')

    time_window_start = models.DateTimeField()
    time_window_end = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()

    evaluation_type = models.CharField(max_length=10, choices=EVALUATION_TYPE_CHOICES, default='auto')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')

    allowed_users = models.ManyToManyField(User, related_name='invited_tests', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('text', 'Text Answer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='mcq')
    correct_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}"


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Evaluation'),
        ('evaluated', 'Evaluated'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_submissions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('test', 'user') 

    def __str__(self):
        return f"{self.user} - {self.test.title}"


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer to {self.question.text[:50]}"
