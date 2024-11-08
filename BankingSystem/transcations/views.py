from django.db.models.query import _BaseQuerySet, QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transcations.constant import DEPOSIT, WITHDRAWAL, LOAN, LOAN_PAID
from datetime import datetime
from django.db.models import Sum
from transcations.models import Transcation
from transcations.forms import(
    DepositForm,
    WithdrawForm,
    LoanRequestForm, 
    TranscationDateRangeForm,
)

class TranscationReportView(LoginRequiredMixin, ListView):
    template_name = ''
    model = Transcation
    form_date = {}
    balance = 0
    
    def get(self, request, *args, **kwargs):
        form = TranscationDateRangeForm(request.get or None)
        if form.is_valid():
            self.form_data = form.clean_data
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        
        start_date_str = self.request.get('start_date')
        end_date_str = self.request.get('end_date')
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%y-%m-%d').date()
            queryset = queryset.filter(timestamp_date_gte = start_date, timestamp_date_lte = end_date)
            self.balance = Transcation.objects.filter(
                timestamp_date_gte = start_date, timestamp_date_lte = end_date
            ).aggregate(Sum('amount'))['amount_sum']
        else:
            self.balance = self.request.user.account.balance
        return queryset.distinct()
    
    def get_context_data(self, **kwarge):
        context = super().get_context_data(**kwarge)
        
        context.update({
            'account': self.request.user.account,
            'form': TranscationDateRangeForm(self.request.GET or None)
        })
        return context

class TranscationCreateMixin(LoginRequiredMixin, CreateView):
    template_name = ''
    model = Transcation
    title = ''
    success_url = reverse_lazy('')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context

class DepositMoneyView(TranscationCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.amount
        
        if not account.initial_deposit_time:
            now = timezone.now()
            account.initial_deposit_time = now
        account.balance += amount
        account.save(
            update_fields = {
                'initial_deposit_time',
                'balance'
            }
        )
        messages.success(
            self.request, f'Deposit Success!'
        )
        return super().form_valid(form)

class WithdrawMoneyView(TranscationCreateMixin):
    form_class = DepositForm
    title = 'Withdraw'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        
        self.request.user.account.balance -= form.cleaned_data.get('ampunt')
        self.request.user.account.save(update_fields = ['balance'])
        
        messages.success(
            self.request, f'Withdraw Success!'
        )
        return super().form_valid(form)
    
class LoanRequestView(TranscationCreateMixin):
    form_class = DepositForm
    title = 'Loan Request'
    
    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_Loan_count = Transcation.objects.filter(
            account = self.request.user.count, transaction_type = 3, loan_approve = True
        ).count()
        
        if current_Loan_count >= 3:
            return HttpResponse("You have crossed Loan Limit")
        messages.success(
            self.request, f'Loan Request submitted'
        )
        return super().form_valid(form)
    
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transcation, id = loan_id)
        
        if loan.loan_approve:
            user_account = loan.account
            
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transcation = user_account.balance
                user_account.save()
                loan.loan_approve = True
                loan.transcation_type = LOAN_PAID
                loan.save()
                return redirect('transactions:loan_list')
            else:
                messages.error(self.request, f'Loan amount is Greater than availabler balance!')
            return redirect('transactions:loan_list')

class LoanListaview(LoginRequiredMixin, ListView):
    model = Transcation
    template_name = ''
    context_object_name = 'loans'
    
    def get_queryset(self):
        user_account = self.request.user.account
        
        querySet = Transcation.objects.filter(account = user_account, transaction_type = 3)
        print(querySet)
        return querySet
        