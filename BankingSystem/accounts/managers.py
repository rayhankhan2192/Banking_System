from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib import auth

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_user(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("You are not a Admin User!")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("You are not a Super User!")
        return self._create_user(email, password, **extra_fields)