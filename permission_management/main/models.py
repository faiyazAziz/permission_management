    # core/models.py
from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    action = models.CharField(max_length=100)
    action_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"{self.action} by {self.user}"


# core/models.py
from django.db import models
from django.contrib.auth.models import User

class ReportData(models.Model):
    report_name = models.CharField(max_length=100)
    report_description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_name
