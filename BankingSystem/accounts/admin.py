from django.contrib import admin

from .models import *

admin.site.register(BankAccountType)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)
