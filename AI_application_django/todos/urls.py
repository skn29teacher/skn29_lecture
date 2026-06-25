from django.urls import path
from . import views
from . import api_views # API 뷰 모듈 추가 임포트

app_name = 'todos'

urlpatterns = [
    # 기존 HTML 템플릿용 뷰 매핑
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # 신규 추가: REST API 백엔드 호출 전용 매핑 경로
    path('api/', api_views.TodoListAPIView.as_view(), name='api_todo_list'),
    path('api/<int:pk>/', api_views.TodoDetailAPIView.as_view(), name='api_todo_detail'),
]