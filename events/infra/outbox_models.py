from django.db import models

class OutboxEvent(models.Model):
    aggregate_type = models.CharField(max_length=50)
    aggregate_id = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)