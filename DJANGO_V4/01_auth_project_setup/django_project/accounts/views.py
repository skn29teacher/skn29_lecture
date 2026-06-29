from django.shortcuts import render, redirect
from .forms import CustomerUserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerUserCreationForm

def home(request):
    return render(request,'main.html')

def signup(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
    else:
        # 빈폼 생성
        form = CustomerUserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

# 가입완료 안내 페이지 
def signup_success(request):
    return render(request,'accounts/signup_success.html')

# 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

# 로그아웃
def logout_view(request):
    # 현재 세션데이터를 데이터베이스에서 만료시키고 쿠키를 삭제
    auth_logout(request)
    return request('home')

