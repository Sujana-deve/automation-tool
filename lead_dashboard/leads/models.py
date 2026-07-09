from django.db import models


class UploadBatch(models.Model):
    """One CSV upload = one batch, so old batches don't mix with new ones."""
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at:%Y-%m-%d %H:%M})"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("Hot", "Hot"),
        ("Warm", "Warm"),
        ("Cold", "Cold"),
    ]

    batch = models.ForeignKey(UploadBatch, on_delete=models.CASCADE, related_name="leads")

    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    opened_email = models.BooleanField(default=False)
    visited_site = models.BooleanField(default=False)
    filled_form = models.BooleanField(default=False)

    opened_email_date = models.DateField(null=True, blank=True)
    visited_site_date = models.DateField(null=True, blank=True)
    filled_form_date = models.DateField(null=True, blank=True)

    score = models.FloatField(default=0)
    score_reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Cold")

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.name} ({self.status}, {self.score})"
