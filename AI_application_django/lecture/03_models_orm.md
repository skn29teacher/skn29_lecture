# 모델과 ORM 및 마이그레이션

장고 모델을 사용하여 데이터베이스 스키마를 정의하고, 마이그레이션을 통해 적용하는 구체적인 명령어 및 장고 ORM을 사용한 데이터 입출력(CRUD) 소스코드를 학습합니다.

---

## 1. Django 모델 작성 방법

모델은 `django.db.models.Model`을 상속받아 클래스로 선언합니다. 클래스 변수가 곧 데이터베이스 테이블의 컬럼명이 됩니다.

### 모델 정의 예제 (todos/models.py)
```python
from django.db import models

class Todo(models.Model):
    # max_length: 필수 지정 속성으로, 저장할 수 있는 문자열의 최대 크기 제한
    title = models.CharField(max_length=200)
    
    # blank=True: 폼 검사 시 값을 기입하지 않고 빈 값으로 두는 것을 허용
    content = models.TextField(blank=True)
    
    # default=False: 데이터를 최초 등록 시 별도 입력을 안 주면 기본값 False 지정
    is_completed = models.BooleanField(default=False)
    
    # auto_now_add=True: 레코드가 최초 생성(Insert)될 때 현재 시간 자동 기록
    created_at = models.DateTimeField(auto_now_add=True)
    
    # auto_now=True: 레코드가 수정(Save/Update)될 때마다 현재 시간 자동 갱신
    updated_at = models.DateTimeField(auto_now=True)

    # 객체를 문자열로 표현할 때 기본 출력값을 지정하는 메소드
    def __str__(self):
        return self.title
```

---

## 2. 마이그레이션 세부 동작 명령어

작성한 모델 정보를 데이터베이스 엔진에 전달하여 실제 테이블을 구성하는 2단계 파이프라인 절차입니다.

### 1단계: 마이그레이션 파일 설계도 생성
`models.py` 내부의 클래스 설계를 분석하여 변경사항을 기록한 파이썬 스크립트 도면을 만듭니다.
```bash
python manage.py makemigrations
```
- 실행 후 `todos/migrations/0002_todo.py` 와 같이 이름 붙여진 파이썬 자동 생성 도면 파일이 생겨납니다.

### 2단계: 데이터베이스에 마이그레이션 적용
작성된 도면 파일을 해석하여 데이터베이스 상에 테이블을 최종 배포합니다.
```bash
python manage.py migrate
```
- 실행 시 장고는 프로젝트 루트에 세팅된 SQLite3 데이터베이스(`db.sqlite3`)에 `todos_todo`라는 명칭으로 테이블을 완성합니다.

---

## 3. Django ORM 데이터 가공 (CRUD) 소스코드 가이드

파이썬 코드만으로 데이터베이스 데이터를 자유롭게 조작하는 구체적인 명령 구문입니다.

### 데이터 삽입 (Create)
```python
# 방법 A: 인스턴스를 직접 생성하여 save() 실행
new_todo = Todo(title="개발 서적 읽기", content="20페이지 분량 학습")
new_todo.save()  # 이 순간 DB에 SQL INSERT 구문이 가동됩니다.

# 방법 B: objects 매니저의 create 메소드 이용 (save 생략 가능)
created_todo = Todo.objects.create(
    title="장고 공부하기",
    content="ORM 기초 챕터 연습"
)
```

### 데이터 조회 (Read)
```python
# 1. 테이블 내 모든 레코드 가져오기
all_list = Todo.objects.all()

# 2. 특정 조건 필터링 (다수의 QuerySet 반환)
completed_list = Todo.objects.filter(is_completed=True)

# 3. 단일 고유 행 가져오기 (만약 매칭값이 없거나 2개 이상이면 에러 발생)
single_todo = Todo.objects.get(id=1)

# 4. 정렬하여 가져오기 (필드명 앞 마이너스'-'는 내림차순 정렬)
sorted_list = Todo.objects.all().order_by('-created_at')
```

### 데이터 수정 (Update)
```python
# 대상 데이터를 먼저 get으로 조회해 온 뒤 필드 값을 수정하고 save()를 호출합니다.
todo_to_edit = Todo.objects.get(id=1)
todo_to_edit.title = "제목 변경하기"
todo_to_edit.is_completed = True
todo_to_edit.save()  # DB에 SQL UPDATE 구문이 가동됩니다.
```

### 데이터 삭제 (Delete)
```python
# 삭제할 데이터 객체를 불러온 뒤 delete() 메소드를 작동시킵니다.
todo_to_delete = Todo.objects.get(id=2)
todo_to_delete.delete()  # 즉시 데이터가 삭제 처리됩니다.
```
