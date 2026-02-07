from django.db import models


class AccountModel(models.Model):
    user_id: models.IntegerField = models.IntegerField(unique=True)
    country_code: models.CharField = models.CharField(
        max_length=2, null=True, blank=True
    )
    currency: models.CharField = models.CharField(max_length=3, null=True, blank=True)
    annual_income: models.DecimalField = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    monthly_investable_amount: models.DecimalField = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
