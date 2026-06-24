from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def todo_list_welcom(request):
    # request : 클라이언트로 부터 들어온 HTTP 요청 메타데이터가 담긴 객체
    # HttpResponse : 클라이언트 브라우저 텍스트나 html을 담아 내보내는 객체   
    return HttpResponse("<h3>할일 관리 애플리케이션 방문을 환영합니다.<p>(함수기반 뷰)</p></h3>")

class AboutView(View):
    # 클라이언트가 get 요청을 보냈을때 자동으로 실행되는 메소드
    def get(self,request):
        return HttpResponse("이 애플리케이션은 사용자 기반의 할일 관리 웹앱입니다.(클래스 뷰 기반)")
    # 클라이언트가 post 요청을 보냈을때 자동으로 실행되는 메소드
    def post(self, request):
        return HttpResponse('데이터가 제출되었습니다.')