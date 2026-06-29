from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password/', views.password_change_view, name='password_change'),
    path('session/', views.session_info_view, name='session_info'),
    path('notice/', views.notice_list_view, name='notice_list'),
    path('notice/create/', views.notice_create_view, name='notice_create'),
]
