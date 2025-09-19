from django.db import models
from datetime import timedelta
from django.utils import timezone


class SessionType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SessionDuration(models.Model):
    label = models.CharField(max_length=50, unique=True)
    duration_minutes = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.label

    def get_timedelta(self):
        return timedelta(minutes=self.duration_minutes)


class SessionFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LeadershipSessionBooking(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    preferred_datetime = models.DateTimeField()
    timezone = models.CharField(max_length=50)

    session_type = models.ForeignKey(SessionType, on_delete=models.PROTECT)
    session_duration = models.ForeignKey(SessionDuration, on_delete=models.PROTECT)
    session_format = models.ForeignKey(SessionFormat, on_delete=models.PROTECT)

    goals = models.TextField(blank=True, null=True)
    referral_source = models.CharField(max_length=100, blank=True, null=True)
    linkedin_or_website = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_mentor_confirmed = models.BooleanField(default=False)
    is_session_completed = models.BooleanField(default=False)
    is_session_held = models.BooleanField(null=True, blank=True)

    mentor_confirmation_token = models.CharField(max_length=64, blank=True, null=True)
    session_completion_token = models.CharField(max_length=64, blank=True, null=True)
    token_generated_at = models.DateTimeField(auto_now_add=True)

    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.full_name} – {self.preferred_datetime.strftime('%Y-%m-%d %H:%M')}"
        )

    def get_session_end_datetime(self):
        if self.session_duration:
            return self.preferred_datetime + self.session_duration.get_timedelta()
        return self.preferred_datetime

    def is_token_valid(self, hours=48):
        expiry_time = self.token_generated_at + timedelta(hours=hours)
        return timezone.now() <= expiry_time


class SendMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.full_name} ({self.email})"
