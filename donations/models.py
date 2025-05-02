# donations/models.py
from django.db import models
from accounts.models import CustomUser

class Donation(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation #{self.id} - {self.amount} BDT"