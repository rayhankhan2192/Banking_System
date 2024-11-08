from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import (MinValueValidator, MaxValueValidator)
from .managers import UserManager
from .constant import GENDER_CHOICE

class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=True)
    is_staff = models.BooleanField(default=False)  # Add this field
    is_superuser = models.BooleanField(default=False)  # Add this field
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        """Check if the user has a specific permission."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Check if the user has permissions for a specific app."""
        return self.is_superuser
    
    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0

class BankAccountType(models.Model):
    name = models.CharField(max_length=30)
    max_withdraw_ammount = models.DecimalField(decimal_places=2, max_digits=10)
    
    def __str__(self):
        return self.name
    
class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User, 
        related_name='account', 
        on_delete=models.CASCADE)
    
    account_type = models.ForeignKey(
        BankAccountType, 
        related_name='accounts', 
        on_delete=models.CASCADE)
    
    account_number = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birthday = models.DateField(null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    initial_deposit_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.account_number)

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post_code = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.email
    