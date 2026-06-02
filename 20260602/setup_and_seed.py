import sqlite3
import random

DB_FILE = r"C:\skn29_자연어\20260602\database.db"

def migrate_table():
    """기존 emp 테이블에 컬럼 추가 (이미 있으면 스킵)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 현재 컬럼 목록 확인
    cursor.execute("PRAGMA table_info(emp)")
    existing_cols = {row[1] for row in cursor.fetchall()}
    print(f"[INFO] 현재 컬럼: {existing_cols}")

    migrations = [
        ("department", "ALTER TABLE emp ADD COLUMN department TEXT"),
        ("position",   "ALTER TABLE emp ADD COLUMN position TEXT"),
        ("salary",     "ALTER TABLE emp ADD COLUMN salary INTEGER"),
        ("age",        "ALTER TABLE emp ADD COLUMN age INTEGER"),
    ]
    for col_name, sql in migrations:
        if col_name not in existing_cols:
            cursor.execute(sql)
            print(f"[OK] 컬럼 추가: {col_name}")
        else:
            print(f"[SKIP] 이미 존재: {col_name}")

    conn.commit()
    conn.close()


def insert_dummy_data(count: int = 100):
    """가상의 직원 데이터를 count건 삽입"""
    names = [
        "김민준", "이서연", "박도윤", "최지우", "정하준",
        "강서현", "조민서", "윤예준", "장수아", "임현우",
        "오지민", "한예린", "신동혁", "권나은", "황태양",
        "송지호", "안서윤", "유준혁", "남지아", "백찬우"
    ]
    departments = ["개발팀", "마케팅팀", "영업팀", "인사팀", "기획팀", "디자인팀", "운영팀"]
    positions   = ["사원", "주임", "대리", "과장", "차장", "부장"]
    salary_range = {
        "사원": (2800, 3500), "주임": (3200, 4000), "대리": (3800, 4800),
        "과장": (4500, 6000), "차장": (5500, 7000), "부장": (6500, 9000)
    }

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    rows = []
    for _ in range(count):
        name       = random.choice(names) + str(random.randint(1, 999))
        department = random.choice(departments)
        position   = random.choice(positions)
        salary     = random.randint(*salary_range[position]) * 1000
        age        = random.randint(24, 58)
        rows.append((name, department, position, salary, age))

    cursor.executemany(
        "INSERT INTO emp (name, department, position, salary, age) VALUES (?, ?, ?, ?, ?)",
        rows
    )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM emp")
    total = cursor.fetchone()[0]
    conn.close()
    print(f"[OK] 더미 데이터 {count}건 삽입 완료 (전체 레코드 수: {total}건)")


def show_sample():
    """삽입된 데이터 샘플 10건 출력"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emp ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    print("\n[샘플 데이터 최근 10건]")
    print(f"{'ID':<5} {'이름':<12} {'부서':<10} {'직급':<6} {'급여':>10} {'나이':>5}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<10} {row[3]:<6} {row[4]:>10,} {row[5]:>5}")


if __name__ == "__main__":
    migrate_table()
    insert_dummy_data(100)
    show_sample()
