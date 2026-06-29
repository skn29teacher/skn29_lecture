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
            # 주소창에 ?next=/accounts/profile/ next 파라메터가 있는지 검사
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

# 로그아웃
def logout_view(request):
    # 현재 세션데이터를 데이터베이스에서 만료시키고 쿠키를 삭제
    auth_logout(request)
    return redirect('home')

# 보호대상 뷰(마이페이지)
from django.contrib.auth.decorators import login_required
@login_required  # 로그인하지 않은 방문자는 settings.py의 LOGIN_URL로 리다이렉션 처리
def profile_view(request):
    return render(request, 'accounts/profile.html')

