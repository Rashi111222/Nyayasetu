from django.db import models
from django.contrib.auth.models import User

class Judgment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    case_number = models.CharField(max_length=200, blank=True)
    uploaded_pdf = models.FileField(upload_to='judgments/')
    raw_text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_number} — {self.status}"


class ActionPlan(models.Model):
    judgment = models.OneToOneField(Judgment, on_delete=models.CASCADE, related_name='action_plan')
    case_number = models.CharField(max_length=200)
    court_name = models.CharField(max_length=300)
    judgment_date = models.CharField(max_length=50, blank=True)
    parties = models.CharField(max_length=500, blank=True)
    judgment_summary = models.TextField(blank=True)
    directives = models.JSONField(default=list)
    compliance_deadline = models.CharField(max_length=100, blank=True)
    appeal_recommended = models.BooleanField(default=False)
    appeal_reason = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan for {self.case_number}"


class OfficerReview(models.Model):
    action_plan = models.OneToOneField(ActionPlan, on_delete=models.CASCADE, related_name='review')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField()
    notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Approved" if self.approved else "Rejected"
        return f"{status} by {self.reviewed_by}"