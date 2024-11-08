from django.db import models

from accounts.models import UserBankAccount
from .constant import TRANSCATION_TYPE_CHOICE


class Transcation(models.Model):
    account = models.ForeignKey(UserBankAccount, related_name='transcations', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    balance_after_transcation = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)
    transcation_type = models.PositiveIntegerField(choices=TRANSCATION_TYPE_CHOICE, null=True)
    
    class Meta:
        ordering = ['timestamp']