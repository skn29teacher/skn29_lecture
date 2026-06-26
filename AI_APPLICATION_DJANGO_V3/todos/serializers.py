from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    # ReadOnlyField: 유저 이름 필드를 읽기 전용(ReadOnly)으로 직렬화해 출력에 결합
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        # 1. 직렬화의 타겟이 되는 데이터베이스 모델 클래스 지정
        model = Todo
        
        # 2. JSON 데이터로 묶어 송수신할 컬럼 명칭 리스트 정의
        fields = [
            'id', 'author', 'author_username', 'title', 
            'content', 'image', 'is_completed', 'created_at', 'updated_at'
        ]
        
        # 3. 데이터 쓰기(POST/PUT) 요청 시 사용자 직접 수정을 막고 시스템이 자동 입력할 읽기전용 필드들 설정
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']