from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name='닉네임')
    def __str__(self):
        return self.username
    
# 공지사항 모델 선언
class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at =  models.DateTimeField("작성일시", auto_now_add=True)
    class Meta:
        # 커스텀 권한 추가 등록(['권한코드네임','권한설명'])
        permissions = [
            ("can_publish_notice",'공지사항 발행 가능 권한'),    # 권한 적용 뷰 : can_publish_notice 권한소유자만 허가
        ]
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 목록'
    def __str__(self):
        return self.title