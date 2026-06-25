from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Todo

# 1. Custom User 모델의 속성 커스터마이징 등록
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # 목록 화면에 표시할 컬럼 지정
    list_display = ['username', 'email', 'nickname', 'is_staff']
    # 상세 정보 조회/수정 화면에서 닉네임 필드 레이아웃 추가
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname',)}),
    )
    # 회원 생성 화면(새 유저 등록) 시 닉네임 필드 레이아웃 추가
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname',)}),
    )

# 2. Todo 관리자 화면 커스터마이징 등록
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['title', 'content']

# 장고 어드민에 맵핑 클래스와 함께 모델 최종 등록
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Todo, TodoAdmin)