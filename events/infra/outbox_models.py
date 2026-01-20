from django.db import models

# Infra DB
# OutboxEventRepository.save() -> OutboxEvent Table
class OutboxEvent(models.Model):
    event_id = models.CharField(max_length=36, unique=True)
    aggregate_type = models.CharField(max_length=50)
    aggregate_id = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)