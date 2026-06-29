from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser

class CustomerUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('추가정보', {'fields':('nickname',)}),
    )
    # 목록화면
    list_display = ['username','email','nickname','is_staff','is_active']
admin.site.register(CustomerUser,CustomerUserAdmin)