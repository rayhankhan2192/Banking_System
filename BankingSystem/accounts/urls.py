from django.urls import path

from .views import UserRegistrationView, LogOutView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('logout/', LogOutView.as_view(), name='user_logout'),
    path('login/', UserRegistrationView.as_view(), name='user_login'),
    
]