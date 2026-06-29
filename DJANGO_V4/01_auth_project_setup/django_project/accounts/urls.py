# http://127.0.0.1:8000/accounts/
from django.urls import path
from . import views
urlpatterns = [    
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success')    
]