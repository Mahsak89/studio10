
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SERVICE_CHOICES = (
    ("Business Strategy Development", "Business Strategy Development"),
    ("Financial Planning and Analysis", "Financial Planning and Analysis"),
    ("Market Research and Analysis", "Market Research and Analysis"),
    ("Process Optimization", "Process Optimization"),
    ("Leadership Development", "Leadership Development"),
    ("Change Management", "Change Management"),
    ("consulting", "consulting"),
)
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("4 PM", "4 PM"),
    ("5 PM", "5 PM"),
)


class Appointment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(
        max_length=50, choices=SERVICE_CHOICES, default="Business Strategy Development")
    day = models.DateField(default=datetime.now)
    time = models.CharField(
        max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
