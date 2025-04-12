from django.db import models
from django.utils import timezone

# Create your models here.

class PageView(models.Model):
    url = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['timestamp']),
        ]

class CalculatorUsage(models.Model):
    calculator_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    input_data = models.JSONField(null=True, blank=True)  # Store the input parameters

    class Meta:
        indexes = [
            models.Index(fields=['calculator_name']),
            models.Index(fields=['timestamp']),
        ]
