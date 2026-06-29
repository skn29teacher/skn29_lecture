from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 기존 UserAdmin 필드셋에 커스텀 필드(nickname)를 추가
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('nickname',)}),
    )
    # 사용자 목록 화면에 노출할 필드 지정
    list_display = ['username', 'email', 'nickname', 'is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
