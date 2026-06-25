from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. Django 기본 User 모델을 확장하여 nickname 필드가 추가된 Custom User 정의
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username

# Create your models here.
class Todo(models.Model):
    # settings.AUTH_USER_MODEL을 외래키의 대상 모델로 지정하여 Custom User를 바인딩합니다.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos',
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=200)
    # 폼 검사시 값이 비어있어도 허용
    content = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    # 최초 레코드(row) 가 생성될때(insert) 자동으로 현재시간 등록
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정(save / update)때마다 현재시간 자동 갱신
    updated_at = models.DateTimeField(auto_now=True)
    #객체를 문자열로 표현할때 기본 출력값을 지정
    def __str__(self):
        return f'id:{self.id} title:{self.title} content:{self.content} is_completed:{self.is_completed}\
        created_at:{self.created_at} updated_at:{self.updated_at}'