from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP


@shared_task
def detect_suspicious_ips():
    """
    Celery task to detect suspicious IP addresses.
    Runs hourly and flags IPs that:
    1. Exceed 100 requests/hour
    2. Access sensitive paths (e.g., /admin, /login)
    """
    # Calculate time threshold (1 hour ago)
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Get all requests from the last hour
    recent_requests = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    
    # Define sensitive paths
    sensitive_paths = ['/admin', '/login', '/admin/', '/login/']
    
    # Dictionary to track request counts per IP
    ip_request_counts = {}
    # Dictionary to track sensitive path access per IP
    ip_sensitive_access = {}
    
    # Analyze recent requests
    for request in recent_requests:
        ip = request.ip_address
        path = request.path
        
        # Count requests per IP
        if ip not in ip_request_counts:
            ip_request_counts[ip] = 0
        ip_request_counts[ip] += 1
        
        # Check for sensitive path access
        if any(sensitive_path in path for sensitive_path in sensitive_paths):
            if ip not in ip_sensitive_access:
                ip_sensitive_access[ip] = []
            ip_sensitive_access[ip].append(path)
    
    # Flag IPs exceeding 100 requests/hour
    for ip, count in ip_request_counts.items():
        if count > 100:
            reason = f"Exceeded 100 requests/hour ({count} requests)"
            SuspiciousIP.objects.update_or_create(
                ip_address=ip,
                defaults={'reason': reason}
            )
    
    # Flag IPs accessing sensitive paths
    for ip, paths in ip_sensitive_access.items():
        unique_paths = list(set(paths))
        reason = f"Accessed sensitive paths: {', '.join(unique_paths)}"
        SuspiciousIP.objects.update_or_create(
            ip_address=ip,
            defaults={'reason': reason}
        )
    
    return f"Anomaly detection completed. Flagged {len(ip_request_counts)} unique IPs."

