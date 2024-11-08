import datetime
from django import forms
from .models import Transcation


class TranscationForm(forms.ModelForm):
    class Meta:
        
        model = Transcation
        fields = ['amount', 'transcation_type']
        
        def __init__(self, *args, **kwargs):
            self.account = kwargs.pop('account')
            self.fields['transcation_type'].disable = True
            self.fields['transcation_type'].widget = forms.HiddenInput
        
        def save(self, commit = True):
            self.instance.account = self.account
            self.instance.balance_after_transcation = self.account.balance
            return super().save()
            
class DepositForm(TranscationForm):
    def clean_amount(self):
        min_deposit_amount = 5
        amount = self.cleaned_data.get('amount')
        
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'Deposit at least {min_deposit_amount} $'
            )
        return amount

class WithdrawForm(TranscationForm):
    def clean__amount(self):
        account = self.account
        
        min_withdraw_amount = 2
        
        max_withdraw_amount = (
            account.account_type.max_withdraw_ammount
        )
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'Withdraw at least {min_withdraw_amount}'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'Max Withdraw amount {max_withdraw_amount}'
            )
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} in your account! Can not Withdraw!'
            )
        return amount

class LoanRequestForm(TranscationForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount