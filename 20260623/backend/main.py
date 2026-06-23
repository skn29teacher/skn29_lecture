import os
import sqlite3
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Async API Lecture Backend", version="1.0.0")

# CORS 정책 허용 설정 (프론트엔드 포트 3000 통신용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실습 편의상 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "lecture.db"
VALID_TOKEN = 'secret-lecture-token'  # 테스트용인증 토큰

# Pydantic 모델 정의
class PostCreate(BaseModel):
    title: str  # 작성자 이름으로 활용
    body: str   # 방명록 내용으로 활용

class PostUpdate(BaseModel):
    title: str
    body: str

# 데이터베이스 초기화 함수 (최초 구동 시 테이블 생성 및 초기화 데이터 주입)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. 사용자 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        website TEXT,
        company_name TEXT
    )
    """)
    
    # 2. 방명록 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    )
    """)
    
    # 3. 국가 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        common_name TEXT NOT NULL UNIQUE,
        official_name TEXT NOT NULL,
        capital TEXT,
        continent TEXT,
        population INTEGER,
        languages TEXT,
        flag_png TEXT
    )
    """)
    
    # 초기 시드 데이터 주입 (비어있는 경우에만 주입)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users_seed = [
            ("홍길동", "gildong", "hong@abc.com", "010-1234-5678", "gildong.com", "조선상단"),
            ("성춘향", "chunhyang", "sung@abc.com", "010-9876-5432", "chunhyang.com", "남원풍물단"),
            ("이몽룡", "mongryong", "lee@abc.com", "010-5555-5555", "mongryong.com", "한양학당")
        ]
        cursor.executemany("INSERT INTO users (name, username, email, phone, website, company_name) VALUES (?, ?, ?, ?, ?, ?)", users_seed)
        
    cursor.execute("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0] == 0:
        posts_seed = [
            ("홍길동", "자바스크립트 비동기 프로그래밍 공부 중입니다."),
            ("성춘향", "FastAPI 백엔드와 SQLite3 데이터베이스 연동 테스트 완료.")
        ]
        cursor.executemany("INSERT INTO posts (title, body) VALUES (?, ?)", posts_seed)
        
    cursor.execute("SELECT COUNT(*) FROM countries")
    if cursor.fetchone()[0] == 0:
        countries_seed = [
            ("South Korea", "Republic of Korea", "Seoul", "Asia", 51780579, "Korean", "https://flagcdn.com/w320/kr.png"),
            ("Japan", "Japan", "Tokyo", "Asia", 125800000, "Japanese", "https://flagcdn.com/w320/jp.png"),
            ("United States", "United States of America", "Washington, D.C.", "North America", 331002651, "English", "https://flagcdn.com/w320/us.png"),
            ("Canada", "Canada", "Ottawa", "North America", 38005238, "English, French", "https://flagcdn.com/w320/ca.png"),
            ("France", "French Republic", "Paris", "Europe", 67391582, "French", "https://flagcdn.com/w320/fr.png"),
            ("Germany", "Federal Republic of Germany", "Berlin", "Europe", 83240525, "German", "https://flagcdn.com/w320/de.png"),
            ("United Kingdom", "United Kingdom of Great Britain and Northern Ireland", "London", "Europe", 67215293, "English", "https://flagcdn.com/w320/gb.png"),
            ("Brazil", "Federative Republic of Brazil", "Brasília", "South America", 212559417, "Portuguese", "https://flagcdn.com/w320/br.png"),
            ("Australia", "Commonwealth of Australia", "Canberra", "Oceania", 25687041, "English", "https://flagcdn.com/w320/au.png"),
            ("India", "Republic of India", "New Delhi", "Asia", 1380004385, "Hindi, English", "https://flagcdn.com/w320/in.png")
        ]
        cursor.executemany("""
        INSERT INTO countries (common_name, official_name, capital, continent, population, languages, flag_png)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, countries_seed)
        
    conn.commit()
    conn.close()

# 앱 시작 시 DB 초기화 실행
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================================================
# 1. 사용자 API 엔드포인트 (4차시, 8차시 연계)
# ==========================================================================

@app.get("/api/users")
def read_users(search: Optional[str] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()

    if search :        
        cursor.execute("SELECT * FROM users WHERE name LIKE ? OR username LIKE ?",
            (f"%{search}%", f"%{search}%")
            );    
    else:
        cursor.execute("SELECT * FROM users ");    
    
    rows = cursor.fetchall()
    conn.close()
    
    users = []
    for row in rows:
        users.append({
            "id": row["id"],
            "name": row["name"],
            "username": row["username"],
            "email": row["email"],
            "phone": row["phone"],
            "website": row["website"],
            "company": {
                "name": row["company_name"]
            }
        })
    return users

@app.get("/api/users/{user_id}")
def read_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"해당 ID({user_id})의 사용자를 찾을 수 없습니다."
        )
        
    return {
        "id": row["id"],
        "name": row["name"],
        "username": row["username"],
        "email": row["email"],
        "phone": row["phone"],
        "website": row["website"],
        "company": {
            "name": row["company_name"]
        }
    }

# ==========================================================================
# 2. 방명록 CRUD API 엔드포인트 (5차시, 8차시 연계)
# ==========================================================================

@app.get("/api/posts")
def read_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    posts_list = []
    for row in rows:
        posts_list.append({
            "id": row["id"],
            "title": row["title"],
            "body": row["body"]
        })
    return posts_list

@app.post("/api/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    # 유효성 검증 예외 모사 (작성자명이 공백이거나 너무 짧은 경우 DB 에러 유도)
    if len(post.title.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="작성자 이름은 최소 2글자 이상 입력해 주세요."
        )
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, body) VALUES (?, ?)", (post.title, post.body))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"id": new_id, "title": post.title, "body": post.body}

@app.put("/api/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 해당 아이템이 있는지 먼저 검사
    cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="수정할 대상 방명록 글이 존재하지 않습니다."
        )
        
    cursor.execute("UPDATE posts SET title = ?, body = ? WHERE id = ?", (post.title, post.body, post_id))
    conn.commit()
    conn.close()
    
    return {"id": post_id, "title": post.title, "body": post.body}

@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 해당 아이템이 있는지 먼저 검사
    cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="삭제할 대상 방명록 글이 존재하지 않습니다."
        )
        
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "deleted_id": post_id}

# ==========================================================================
# 3. 국가 검색 API 엔드포인트 (7차시, 8차시 연계)
# ==========================================================================

@app.get("/api/countries")
def search_countries(search: Optional[str] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if search:
        # SQLite LIKE를 통한 부분 검색 구현 (영문 국가명 기준)
        cursor.execute(
            "SELECT * FROM countries WHERE common_name LIKE ? OR official_name LIKE ?",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cursor.execute("SELECT * FROM countries")
        
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"검색 결과에 부합하는 국가 정보가 존재하지 않습니다. (검색어: {search})"
        )
        
    countries = []  
    for row in rows:
        # DB 저장용 언어 스트링을 프론트엔드가 요구하는 언어 해시 객체 형태로 변환
        lang_list = [lang.strip() for lang in row["languages"].split(",")]
        lang_dict = {f"lang_{i}": lang for i, lang in enumerate(lang_list)}
        
        countries.append({
            "name": {
                "common": row["common_name"],
                "official": row["official_name"]
            },
            "capital": [row["capital"]],
            "continents": [row["continent"]],
            "population": row["population"],
            "languages": lang_dict,
            "flags": {
                "svg": row["flag_png"],
                "png": row["flag_png"]
            }
        })
    return countries

# ==========================================================================
# 4. 강제 오류 테스트 API 엔드포인트 (5차시, 6차시 연계)
# ==========================================================================

@app.get("/api/error/500")
def force_server_error():
    # 500 Internal Server Error 강제 시뮬레이션
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="가상 데이터베이스 서버 내부에서 치명적인 충돌 오류가 강제 발생했습니다."
    )

@app.get("/api/secure-data")
def read_secure_data(authorization: Optional[str] = Header(None)):
    # 6차시 Axios 헤더 실습 연계용 보안 엔드포인트
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증을 위한 Bearer 토큰이 헤더에 누락되었거나 비정상적입니다."
        )
        
    token = authorization.split(" ")[1]
    if token != VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='제시한 인증토큰이 만료되었거나 비정상적입니다.'
        )

    return {
        "verified": True,
        "token_used": token,
        "secret_message": "보안 연동 인증 통과: SQLite DB 관리자 권한을 획득하였습니다."
    }

if __name__ == "__main__":
    import uvicorn
    # 외부 터미널에서 python backend/main.py 로 직접 실행 가능
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
