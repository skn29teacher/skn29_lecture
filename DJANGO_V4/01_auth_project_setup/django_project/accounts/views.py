from django.shortcuts import render, redirect
from .forms import CustomerUserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages  # 성공/실패 메세지 전달용
from .forms import CustomerUserCreationForm
from .models import Notice

# 비밀번호 변경 뷰
@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 중요 : 비밀번호 해시값 세션 동기화(자동 로그아웃 방지)
            update_session_auth_hash(request,user)
            # 메세지 프레임웍크에 성공알림 추가
            messages.success(request,'비밀번호가 성공적으로 변경되었습니다.')
            return redirect('profile')
        else:
            messages.error(request,'입력 정보를 다시한번 확인해 주세요')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/passowrd_change.html', {'form':form})

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

@login_required  # 로그인하지 않은 방문자는 settings.py의 LOGIN_URL로 리다이렉션 처리
def profile_view(request):
    return render(request, 'accounts/profile.html')

# 새션 진단 및 제어 정보 뷰
@login_required
def session_info_view(request):
    # 세션 키 및 유효성 정보 획득
    session_key = request.session.session_key
    expiry_age = request.session.get_expiry_age() # 남은 수명(초)
    expiry_date = request.session.get_expiry_date() # 만료시점

    context = {
        'session_key' : session_key,
        'expiry_age' : expiry_age,
        'expiry_date' : expiry_date,
        'session_data' : dict(request.session.items())  # 세션에 담긴 정보 딕셔너리 변환
    }
    return render(request,'accounts/session_info.html', context)

#공지사항 목록 조회  : 로그인만 되면 가능
@login_required
def notice_list_view(request):
    notices = Notice.object.all().order_by('-created_at')
    return render(request, 'accounts/notice_list.html', {'notices':notices})

# 공지사항 생성
@permission_required('accounts.can_publish_notice',raise_exception=True)
def notice_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Notice.objects.create(title = title, content=content)
            return redirect('notice_list')
    else:
        return render(request, 'accounts/notice_create.html')


