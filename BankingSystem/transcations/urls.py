from django.urls import path

from .views import *

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='depost_money'),
    path('report/', TranscationReportView.as_view(), name='transaction_report'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw_money'),
    path('loan_request/', LoanRequestForm.as_view(), name='loan_request'),
    path('loans/', LoanListaview.as_view(), name='Loan_List'),
    path('loans/<int:loan_id>/', PayLoanView.as_view(), name='loan_pay'),
    
]