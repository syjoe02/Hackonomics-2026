from django.db import models

class AccountModel(models.Model):
    user_id = models.IntegerField(unique=True) # mapping Django User.id 1:1
    
    country_code = models.CharField(max_length=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    annual_income = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    monthly_investable_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)