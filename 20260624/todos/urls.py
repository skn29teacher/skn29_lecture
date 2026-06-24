"""
URL configuration for todoboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
# 앱의 네임스페이스를 지정해서 템플릿 주소를 역추적할때 식별자로 사용
app_name = 'todos'
urlpatterns = [    
    # 'http://127.0.0.1:8000/  주소요청시 viewes.todo_list_welcom 함수 실행
    path('', views.todo_list_welcom, name='todo_welcome'),
    # 'http://127.0.0.1:8000/about/  주소요청시 viewes.AboutView 클래스 뷰  실행
    path('about/', views.AboutView.as_view(), name='about'),
    path('todos/create', views.todo_create,name='todo_create'),
]
