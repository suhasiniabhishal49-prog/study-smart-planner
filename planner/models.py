from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    """A study subject linked to a user."""
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    color = models.CharField(max_length=7, default='#3b82f6')  # hex color
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """A study task linked to a subject and user."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    estimated_time = models.IntegerField(default=30, help_text='Estimated time in minutes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Returns True if task is still pending but deadline has passed."""
        return self.status == 'Pending' and self.deadline < timezone.now()


class StudySchedule(models.Model):
    """An auto-generated study schedule slot."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='scheduled_slots')
    date = models.DateField()
    allocated_minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.task.title} on {self.date}"
