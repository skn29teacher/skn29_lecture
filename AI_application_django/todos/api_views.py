from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Todo
from .serializers import TodoSerializer

# 1. 목록 조회 및 신규 생성 API 뷰
class TodoListAPIView(APIView):
    # 로그인 인증을 거친 검증된 클라이언트의 요청만 이 API에 진입할 수 있도록 허용합니다.
    permission_classes = [permissions.IsAuthenticated]

    # HTTP GET: 현재 로그인한 사용자가 등록한 할일들만 역순으로 조회하여 직렬화 전달
    def get(self, request):
        todos = Todo.objects.filter(author=request.user).order_by('-created_at')
        # many=True: 쿼리셋 목록 데이터를 다량 직렬화할 때 필수 옵션
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    # HTTP POST: 데이터 검증 후 신규 할일 객체 데이터베이스 영구 등록
    def post(self, request):
        # request.data를 직렬화기 생성자의 첫 인자로 주입하여 데이터를 바인딩
        serializer = TodoSerializer(data=request.data)
        
        if serializer.is_valid():
            # 저장(save)을 가동하면서 직렬화기 바깥에 있는 작성자(author) 속성에 현재 로그인 세션 계정 수동 지정
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # 유효성 검사를 넘지 못하면 400 Bad Request와 에러 항목 메시지 JSON 리턴
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. 개별 상세 조회, 수정, 삭제 API 뷰
class TodoDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 타겟 데이터의 식별과 계정 소유 권한을 조율하는 전처리기 도우미 함수
    def get_object(self, pk, user):
        todo = get_object_or_404(Todo, pk=pk)
        # 만약 본인의 데이터가 아니라면 403 Forbidden 권한 에러 방출
        if todo.author != user:
            self.permission_denied(self.request, message="본인의 할일이 아닙니다.")
        return todo

    # HTTP GET: 단일 데이터 상세 상세 조회
    def get(self, request, pk):
        todo = self.get_object(pk, request.user)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    # HTTP PUT: 단일 데이터 수정
    def put(self, request, pk):
        todo = self.get_object(pk, request.user)
        # 기존 Todo 인스턴스 정보와 새로 전달받은 입력 본문을 결합하여 수정 폼 직렬화기 로드
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # HTTP DELETE: 데이터 영구 삭제
    def delete(self, request, pk):
        todo = self.get_object(pk, request.user)
        todo.delete()
        # 성공적으로 지워졌음을 알리는 204 No Content 리턴
        return Response(status=status.HTTP_204_NO_CONTENT)