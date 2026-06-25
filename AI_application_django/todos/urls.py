from django.urls import path
from . import views
from . import api_views

app_name = 'todos'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # 신규 추가: REST API 백엔드 호출 전용 매핑 경로
    path('api/', api_views.TodoListAPIView.as_view(), name='api_todo_list'),
    path('api/<int:pk>/', api_views.TodoDetailAPIView.as_view(), name='api_todo_detail'),
]