from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Todo  # 데이터베이스 테이블
from .forms import TodoForm  # 폼유효성 검사

def todo_list(request):
    # 등록된 전체 할 일을 최신순으로 가져와 리스트 템플릿에 전달
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todos/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        # 사용자가 폼에 채워 전송(POST)한 원시 데이터를 폼 인스턴스에 밀어 넣습니다.
        form = TodoForm(request.POST)
        # 데이터 유효성(빈 값 검사, 글자 수 한도, 형식 일치 등)을 점검합니다.
        if form.is_valid():
            # 유효성 검증을 통과한 데이터를 DB에 저장합니다.
            form.save()
            # 저장 완료 후 목록 화면으로 리다이렉트합니다.
            return redirect('todos:todo_list')
    else:
        # GET 요청일 때는 입력을 위한 빈 폼 객체를 생성합니다.
        form = TodoForm()
        
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '등록'})

def todo_update(request, pk):
    # 수정할 대상을 기본 키(pk)로 조회
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        # 기존 인스턴스(instance=todo)에 새로운 POST 데이터를 덮어씌웁니다.
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos:todo_list')
    else:
        # 수정 화면 조회 시 기존 값을 채워 폼을 생성합니다.
        form = TodoForm(instance=todo)
        
    return render(request, 'todos/todo_form.html', {'form': form, 'action': '수정'})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # POST 방식으로 요청이 들어오면 삭제를 처리합니다.
    if request.method == 'POST':
        todo.delete()
    return redirect('todos:todo_list')

class AboutView(View):
    def get(self, request):
        return render(request, 'todos/about.html')