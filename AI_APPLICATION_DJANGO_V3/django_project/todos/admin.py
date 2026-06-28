from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'nickname', 'is_staff']
    # 어드민 상세 보기 화면의 필드 셋 그룹에 avatar 항목을 추가 등록합니다.
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', 'avatar')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)