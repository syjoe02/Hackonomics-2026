from django.db import models


# Stored news per country, not per user
class BusinessNewsModel(models.Model):
    country_code: models.CharField = models.CharField(max_length=10, db_index=True)
    content: models.JSONField = models.JSONField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "business_news"
        ordering = ["-created_at"]
