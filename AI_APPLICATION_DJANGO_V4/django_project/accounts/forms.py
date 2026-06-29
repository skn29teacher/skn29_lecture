from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # 이메일을 필수 입력 필드로 오버라이드
    email = forms.EmailField(required=True, label="이메일")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # 회원가입 시 기입받을 필드를 구성 (기본 필드 + 이메일 + 닉네임)
        fields = UserCreationForm.Meta.fields + ('email', 'nickname')
