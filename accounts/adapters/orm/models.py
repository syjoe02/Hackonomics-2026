from django.db import models

class AccountModel(models.Model):
    user_id = models.IntegerField(unique=True)
    country_code = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    annual_income = models.DecimalField(
        max_digits=15, decimal_places=2
    )
    monthly_investable_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    updated_at = models.DateTimeField(auto_now=True)