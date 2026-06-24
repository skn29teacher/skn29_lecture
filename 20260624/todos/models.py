from django.db import models

# Create your models here.
class Todo(models.Model):
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
        return f'title:{self.title} content:{self.content} created_at:{self.created_at}'
