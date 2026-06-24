from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        # 1. 폼과 1대1로 연동할 데이터 모델 클래스 지정
        model = Todo
        
        # 2. 사용자에게 입력을 받아 처리할 대상 컬럼 리스트 지정
        fields = ['title', 'content', 'is_completed']
        
        # 3. HTML 엘리먼트 렌더링 시 적용할 CSS 클래스 속성 및 Placeholder 설정
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '할 일을 입력하세요 (예: 파이썬 복습하기)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': '상세한 할 일 설명이나 메모를 적어주세요'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }
        
        # 4. 브라우저 화면에 출력될 레이블명 매칭
        labels = {
            'title': '할 일 제목',
            'content': '메모 및 세부내용',
            'is_completed': '완료 상태'
        }