from django.db import models
from django.utils import timezone


class BlockedIP(models.Model):
    """
    Model to store blocked IP addresses.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Blocked IP'
        verbose_name_plural = 'Blocked IPs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ip_address}"


class RequestLog(models.Model):
    """
    Model to store request logs with IP address, timestamp, path, and geolocation data.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"


class SuspiciousIP(models.Model):
    """
    Model to store suspicious IP addresses flagged by anomaly detection.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Suspicious IP'
        verbose_name_plural = 'Suspicious IPs'
        ordering = ['-detected_at']

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"

