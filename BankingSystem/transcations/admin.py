from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from transcations.models import Transcation

admin.register(Transcation)
admin.site.register(Transcation)
class TranscationAdmin(admin.ModelAdmin):
    list_display = [
        'account',
        'amount',
        'balance_after_transcation',
        'transcation_type',
        'loan_approve'

    ]
    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.balance_after_transcation = obj.account.balance
        obj.account.save()
        super().save_model(self, request, obj, form, change)