from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# 1. 디폴트 라우터 초기화
router = DefaultRouter()
# 2. todos 라는 식별자 경로 뒤에 뷰셋 바인딩 등록
router.register('todos', api_views.TodoViewSet, basename='api_todo')

app_name = 'todos'

urlpatterns = [
    # 전통적인 템플릿(HTML) 전용 경로
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/update/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # 신규 추가: SPA 진입점 뷰 경로
    path('spa/', views.spa_index, name='spa_index'),

    # 신규 추가: 라우터가 계산한 REST API 경로 세트 일괄 주입
    # 이 매핑으로 인해 /todos/api/todos/ 및 /todos/api/todos/<pk>/ 주소가 자동 개설됩니다.
    path('api/', include(router.urls)),
]