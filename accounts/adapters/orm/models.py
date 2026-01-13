from django.db import models

class AccountModel(models.Model):
    user_id = models.IntegerField(unique=True)
    country_code = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    annual_income = models.IntegerField()
    monthly_investable_amount = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)