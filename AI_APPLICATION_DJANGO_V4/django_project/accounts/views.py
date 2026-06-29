from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Notice

# 회원가입, 로그인, 로그아웃, 프로필, 비밀번호 변경, 세션 진단 뷰 등 기존 유지...

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'accounts/signup_success.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')

# 통합 대시보드를 위한 홈 뷰 개편
def home(request):
    notices = Notice.objects.all().order_by('-created_at')[:3]  # 최근 3개 공지만
    
    # 세션 진단 정보 획득 (로그인 시에만)
    session_key = None
    expiry_age = None
    expiry_date = None
    if request.user.is_authenticated:
        session_key = request.session.session_key
        expiry_age = request.session.get_expiry_age()
        expiry_date = request.session.get_expiry_date()
    
    context = {
        'notices': notices,
        'session_key': session_key,
        'expiry_age': expiry_age,
        'expiry_date': expiry_date,
    }
    return render(request, 'accounts/home.html', context)

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('profile')
        else:
            messages.error(request, '입력한 비밀번호 정보를 다시 확인해 주세요.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/password_change.html', {'form': form})

@login_required
def session_info_view(request):
    session_key = request.session.session_key
    expiry_age = request.session.get_expiry_age()
    expiry_date = request.session.get_expiry_date()
    
    context = {
        'session_key': session_key,
        'expiry_age': expiry_age,
        'expiry_date': expiry_date,
        'session_data': dict(request.session.items())
    }
    return render(request, 'accounts/session_info.html', context)

@login_required
def notice_list_view(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'accounts/notice_list.html', {'notices': notices})

@login_required
@permission_required('accounts.can_publish_notice', raise_exception=True)
def notice_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Notice.objects.create(title=title, content=content)
            return redirect('notice_list')
    return render(request, 'accounts/notice_create.html')
