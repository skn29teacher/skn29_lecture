from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerUser

#회원가입 전용 커스텀 폼
class CustomerUserCreationForm(UserCreationForm):
    # 이메일을 필수 입력사항으로 정의
    email = forms.EmailField(required=True,label='이메일')
    class Meta:
        model = CustomerUser
        # 회원가입 양식에 노출할 필드 지정
        fields = UserCreationForm.Meta.fields + ('email','nickname')
