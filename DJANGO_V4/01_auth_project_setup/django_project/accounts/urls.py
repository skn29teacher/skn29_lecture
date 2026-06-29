# http://127.0.0.1:8000/accounts/
from django.urls import path
from . import views
urlpatterns = [        
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('/accountssignup/success/', views.signup_success, name='signup_success')    
]