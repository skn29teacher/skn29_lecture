from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Todo

# Create your views here.
def todo_list_welcom(request):
    # request : 클라이언트로 부터 들어온 HTTP 요청 메타데이터가 담긴 객체
    # HttpResponse : 클라이언트 브라우저 텍스트나 html을 담아 내보내는 객체   
    return HttpResponse("<h3>할일 관리 애플리케이션 방문을 환영합니다.<p>(함수기반 뷰)</p></h3>")


def todo_create(request):
    new_todo = Todo(title='개발계획 세우기', content='한달반정도의 기간동안 개발할 내용')
    new_todo.save()  # sql insert가 장고 프레임웍에서 내부적으로 자동으로 변환됨

class AboutView(View):
    # 클라이언트가 get 요청을 보냈을때 자동으로 실행되는 메소드
    def get(self,request):
        return HttpResponse("이 애플리케이션은 사용자 기반의 할일 관리 웹앱입니다.(클래스 뷰 기반)")
    # 클라이언트가 post 요청을 보냈을때 자동으로 실행되는 메소드
    def post(self, request):
        return HttpResponse('데이터가 제출되었습니다.')