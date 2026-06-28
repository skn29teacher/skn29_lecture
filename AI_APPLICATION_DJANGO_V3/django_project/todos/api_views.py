from rest_framework import viewsets, permissions
from .models import Todo
from .serializers import TodoSerializer

# ModelViewSet을 상속하면 목록조회, 신규등록, 상세조회, 전체수정, 부분수정, 삭제 처리가 자동 통합됩니다.
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 로그인 세션에 따라 본인 데이터 쿼리셋만 필터링 후 반환
    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user).order_by('-created_at')

    # 새 할일 등록 시 Serializer가 차단한 author 필드에 현재 요청 유저 자동 삽입
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)