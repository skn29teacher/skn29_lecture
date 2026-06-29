from django.shortcuts import render, redirect
from .forms import CustomerUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
    else:
        # 빈폼 생성
        form = CustomerUserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

# 가입완료 안내 페이지 
def signup_success(request):
    return render(request,'accounts/signup_success.html')

