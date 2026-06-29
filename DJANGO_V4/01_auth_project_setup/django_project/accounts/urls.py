# http://127.0.0.1:8000/accounts/
from django.urls import path
from . import views
urlpatterns = [        
    path('', views.home, name='home'),
    path('notice/',views.notice_list_view,name='notice_list')
    path('notice/create',views.notice_create_view,name='notice_create')
    path('accounts/session', views.session_info_view, name='session_info'),
    path('accounts/password/', views.password_change_view, name='password_change'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/success/', views.signup_success, name='signup_success')
]