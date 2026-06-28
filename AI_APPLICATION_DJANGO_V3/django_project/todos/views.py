from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .models import Todo
from .forms import TodoForm, CustomUserCreationForm

# 1. 로그인한 사용자 본인의 할일 목록만 필터링하여 노출
@login_required
def todo_list(request):
    todos = Todo.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'todos/todo_list.html', {'todos': todos})

# 2. 할일 등록 시 현재 로그인 중인 사용자의 세션 정보(request.user)를 작성자로 주입
@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            # commit=False: DB 인서트 직전에 정보 수집만 수행한 대기 상태 객체 반환
            todo = form.save(commit=False)
            todo.author = request.user # 현재 세션 유저를 작성자로 지정
            todo.save() # 최종 DB에 저장
            return redirect('todos:todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '등록'})

# 3. 작성자가 아니면 수정을 할 수 없도록 보안 통제 추가
@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # 현재 접근한 사용자가 실제 등록자가 아니면 403 금지 에러 반환
    if todo.author != request.user:
        return HttpResponseForbidden("본인의 할일만 수정할 수 있습니다.")
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos:todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '수정'})

# 4. 작성자가 아니면 삭제를 할 수 없도록 보안 통제 추가
@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if todo.author != request.user:
        return HttpResponseForbidden("본인의 할일만 삭제할 수 있습니다.")
    
    if request.method == 'POST':
        todo.delete()
    return redirect('todos:todo_list')

# 5. 회원가입 뷰
def signup(request):
    # 이미 로그인한 상태라면 목록 화면으로 돌려보냅니다.
    if request.user.is_authenticated:
        return redirect('todos:todo_list')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 가입 성공 시 세션 로그인도 원스톱으로 처리
            return redirect('todos:todo_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'todos/signup.html', {'form': form})

# 6. 로그인 뷰
def login_view(request):
    if request.user.is_authenticated:
        return redirect('todos:todo_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # ID / Password의 진위 검증 가동
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user) # 통과된 사용자를 세션에 등록
                return redirect('todos:todo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'todos/login.html', {'form': form})

# 7. 로그아웃 뷰
def logout_view(request):
    auth_logout(request) # 세션 해제 및 세션 쿠키 소멸 처리
    return redirect('todos:login')

class AboutView(View):
    def get(self, request):
        return render(request, 'todos/about.html')
    
@login_required
def spa_index(request):
    # 비동기로 동작하게 될 spa 템플릿 호출
    return render(request, 'todos/spa.html')    