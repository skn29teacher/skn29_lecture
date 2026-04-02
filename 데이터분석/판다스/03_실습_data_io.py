"""
Pandas 데이터 로드 및 저장 실습
세션 3: 다양한 파일 형식 다루기

학습 목표:
1. CSV, Excel, JSON 파일 읽기/쓰기
2. 데이터베이스 연동
3. 다양한 옵션 활용
4. 여러 파일 병합
"""

import pandas as pd
import numpy as np
import sqlite3
import os

print("=" * 60)
print("1. CSV 파일 읽기")
print("=" * 60)

# 1.1 기본 읽기
df_students = pd.read_csv('data/students.csv', encoding='utf-8-sig')
print("\n학생 데이터:")
print(df_students.head())
print(f"Shape: {df_students.shape}")

# 1.2 특정 컬럼만 읽기
df_selected = pd.read_csv('data/students.csv', 
                          usecols=['name', 'math', 'english'],
                          encoding='utf-8-sig')
print("\n특정 컬럼만 읽기:")
print(df_selected.head())

# 1.3 인덱스 컬럼 지정
df_indexed = pd.read_csv('data/students.csv', 
                         index_col='student_id',
                         encoding='utf-8-sig')
print("\nstudent_id를 인덱스로:")
print(df_indexed.head())

# 1.4 데이터 타입 지정
dtypes = {
    'student_id': 'int32',
    'age': 'int8',
    'math': 'int16',
    'english': 'int16',
    'science': 'int16'
}
df_typed = pd.read_csv('data/students.csv', dtype=dtypes, encoding='utf-8-sig')
print("\n데이터 타입 지정:")
print(df_typed.dtypes)

# 1.5 처음 n개 행만 읽기
df_limited = pd.read_csv('data/students.csv', nrows=5, encoding='utf-8-sig')
print("\n처음 5개 행만:")
print(df_limited)


print("\n" + "=" * 60)
print("2. CSV 파일 쓰기")
print("=" * 60)

# 2.1 기본 저장
df_students.to_csv('data/output_basic.csv', index=False, encoding='utf-8-sig')
print("\n✓ output_basic.csv 저장 완료")

# 2.2 특정 컬럼만 저장
df_students.to_csv('data/output_selected.csv', 
                   columns=['name', 'math', 'english'], 
                   index=False,
                   encoding='utf-8-sig')
print("✓ output_selected.csv 저장 완료 (특정 컬럼만)")

# 2.3 구분자 변경
df_students.to_csv('data/output_semicolon.csv', 
                   sep=';', 
                   index=False,
                   encoding='utf-8-sig')
print("✓ output_semicolon.csv 저장 완료 (세미콜론 구분)")


print("\n" + "=" * 60)
print("3. Excel 파일 읽기")
print("=" * 60)

# 3.1 단일 시트 읽기 (기본 - 첫 번째 시트)
df_company = pd.read_excel('data/company_data.xlsx')
print("\n첫 번째 시트 (직원정보):")
print(df_company.head())

# 3.2 특정 시트 읽기 (시트 이름으로)
df_emp = pd.read_excel('data/company_data.xlsx', sheet_name='직원정보')
df_dept = pd.read_excel('data/company_data.xlsx', sheet_name='부서정보')
df_proj = pd.read_excel('data/company_data.xlsx', sheet_name='프로젝트')

print("\n부서정보 시트:")
print(df_dept)

# 3.3 모든 시트 읽기
all_sheets = pd.read_excel('data/company_data.xlsx', sheet_name=None)
print("\n모든 시트 이름:")
for sheet_name in all_sheets.keys():
    print(f"  - {sheet_name}: {all_sheets[sheet_name].shape}")

# 3.4 여러 시트를 한번에
sheets_dict = pd.read_excel('data/company_data.xlsx', 
                            sheet_name=['직원정보', '부서정보'])
print("\n여러 시트 읽기:")
print(f"직원정보: {sheets_dict['직원정보'].shape}")
print(f"부서정보: {sheets_dict['부서정보'].shape}")


print("\n" + "=" * 60)
print("4. Excel 파일 쓰기")
print("=" * 60)

# 4.1 단일 시트 저장
df_students.to_excel('data/output_students.xlsx', 
                     sheet_name='성적표', 
                     index=False)
print("\n✓ output_students.xlsx 저장 완료")

# 4.2 여러 시트 저장
with pd.ExcelWriter('data/output_multi_sheet.xlsx', engine='openpyxl') as writer:
    df_students.to_excel(writer, sheet_name='학생', index=False)
    df_emp.to_excel(writer, sheet_name='직원', index=False)
    df_dept.to_excel(writer, sheet_name='부서', index=False)
print("✓ output_multi_sheet.xlsx 저장 완료 (3개 시트)")


print("\n" + "=" * 60)
print("5. JSON 파일 읽기")
print("=" * 60)

# 5.1 기본 읽기
df_customers = pd.read_json('data/customers.json')
print("\n고객 데이터:")
print(df_customers.head())

# 5.2 orient 지정
df_orders = pd.read_json('data/orders.json', orient='records')
print("\n주문 데이터:")
print(df_orders.head())

print(f"\nShape: {df_orders.shape}")


print("\n" + "=" * 60)
print("6. JSON 파일 쓰기")
print("=" * 60)

# 6.1 기본 저장
df_customers.to_json('data/output_customers.json', 
                     orient='records', 
                     force_ascii=False,
                     indent=2)
print("\n✓ output_customers.json 저장 완료")

# 6.2 다양한 orient 옵션
df_sample = df_students.head(3)

# records 형식
df_sample.to_json('data/output_records.json', 
                  orient='records', 
                  force_ascii=False, 
                  indent=2)

# index 형식
df_sample.to_json('data/output_index.json', 
                  orient='index', 
                  force_ascii=False, 
                  indent=2)

print("✓ 다양한 형식의 JSON 파일 저장 완료")


print("\n" + "=" * 60)
print("7. SQLite 데이터베이스 읽기")
print("=" * 60)

# 7.1 데이터베이스 연결
conn = sqlite3.connect('data/sample_database.db')

# 7.2 테이블 읽기
df_db_students = pd.read_sql('SELECT * FROM students', conn)
print("\nstudents 테이블:")
print(df_db_students.head())

# 7.3 SQL 쿼리 실행
query = """
SELECT name, math, english, science, 
       (math + english + science) / 3.0 as average
FROM students
WHERE math >= 80
ORDER BY math DESC
LIMIT 10
"""
df_query = pd.read_sql(query, conn)
print("\n수학 80점 이상 학생 (상위 10명):")
print(df_query)

# 7.4 제품 테이블 읽기
df_db_products = pd.read_sql('SELECT * FROM products', conn)
print("\nproducts 테이블:")
print(df_db_products.head())

# 7.5 카테고리별 집계 쿼리
query_agg = """
SELECT category, 
       COUNT(*) as product_count,
       AVG(price) as avg_price,
       SUM(stock) as total_stock
FROM products
GROUP BY category
"""
df_agg = pd.read_sql(query_agg, conn)
print("\n카테고리별 집계:")
print(df_agg)

conn.close()


print("\n" + "=" * 60)
print("8. SQLite 데이터베이스 쓰기")
print("=" * 60)

# 8.1 새 데이터베이스 생성
conn = sqlite3.connect('data/new_database.db')

# 8.2 DataFrame을 테이블로 저장
df_students.to_sql('students_new', conn, if_exists='replace', index=False)
print("\n✓ students_new 테이블 생성 완료")

# 8.3 추가 데이터 삽입 (append)
additional_students = pd.DataFrame({
    'student_id': [21, 22, 23],
    'name': ['신입생1', '신입생2', '신입생3'],
    'age': [19, 20, 19],
    'gender': ['남', '여', '남'],
    'math': [85, 90, 78],
    'english': [88, 92, 85],
    'science': [90, 88, 82],
    'grade': ['B', 'A', 'C']
})
additional_students.to_sql('students_new', conn, if_exists='append', index=False)
print("✓ 추가 데이터 삽입 완료")

# 확인
df_verify = pd.read_sql('SELECT * FROM students_new', conn)
print(f"\n총 학생 수: {len(df_verify)}")
print("마지막 3명:")
print(df_verify.tail(3))

conn.close()


print("\n" + "=" * 60)
print("9. 다양한 구분자의 파일 읽기")
print("=" * 60)

# 9.1 탭 구분 파일
df_tab = pd.read_csv('data/tab_separated.txt', sep='\t')
print("\n탭 구분 파일:")
print(df_tab.head())

# 9.2 파이프 구분 파일
df_pipe = pd.read_csv('data/pipe_separated.txt', sep='|')
print("\n파이프 구분 파일:")
print(df_pipe.head())


print("\n" + "=" * 60)
print("10. 여러 CSV 파일 병합")
print("=" * 60)

# 10.1 월별 파일 읽어서 병합
import glob

csv_files = glob.glob('data/orders_2024_*.csv')
print(f"\n발견된 파일: {len(csv_files)}개")
for f in csv_files:
    print(f"  - {os.path.basename(f)}")

# 10.2 모든 파일 읽어서 리스트에 저장
dfs = []
for file in csv_files:
    df = pd.read_csv(file, encoding='utf-8-sig')
    dfs.append(df)
    print(f"✓ {os.path.basename(file)} 읽기 완료: {df.shape}")

# 10.3 병합
df_merged = pd.concat(dfs, ignore_index=True)
print(f"\n병합 결과: {df_merged.shape}")
print("처음 5개 행:")
print(df_merged.head())
print("\n마지막 5개 행:")
print(df_merged.tail())

# 10.4 병합된 데이터 저장
df_merged.to_csv('data/orders_2024_all.csv', index=False, encoding='utf-8-sig')
print("\n✓ orders_2024_all.csv 저장 완료")


print("\n" + "=" * 60)
print("11. 결측치가 있는 데이터 처리")
print("=" * 60)

# 11.1 결측치 포함 파일 읽기
df_incomplete = pd.read_csv('data/incomplete_data.csv', encoding='utf-8-sig')
print("\n결측치 포함 데이터:")
print(df_incomplete.head(10))

# 11.2 결측치 확인
print("\n각 컬럼의 결측치 개수:")
print(df_incomplete.isnull().sum())

# 11.3 결측치 처리 후 저장
df_cleaned = df_incomplete.copy()
df_cleaned['age'] = df_cleaned['age'].fillna(df_cleaned['age'].median())
df_cleaned['salary'] = df_cleaned['salary'].fillna(df_cleaned['salary'].mean())
df_cleaned['name'] = df_cleaned['name'].fillna('Unknown')
df_cleaned['department'] = df_cleaned['department'].fillna('미배정')

print("\n결측치 처리 후:")
print(df_cleaned.isnull().sum())

df_cleaned.to_csv('data/cleaned_data.csv', index=False, encoding='utf-8-sig')
print("\n✓ cleaned_data.csv 저장 완료")


print("\n" + "=" * 60)
print("12. 실전 예제 1: 데이터 ETL 파이프라인")
print("=" * 60)

# 12.1 여러 소스에서 데이터 읽기
print("\n[1단계] 데이터 로드")
students = pd.read_csv('data/students.csv', encoding='utf-8-sig')
products = pd.read_csv('data/products.csv', encoding='utf-8-sig')
print(f"✓ 학생 데이터: {students.shape}")
print(f"✓ 제품 데이터: {products.shape}")

# 12.2 데이터 변환
print("\n[2단계] 데이터 변환")
# 학생 데이터: 총점 및 평균 추가
students['total'] = students['math'] + students['english'] + students['science']
students['average'] = students['total'] / 3
print("✓ 학생 성적 계산 완료")

# 제품 데이터: 재고 가치 계산
products['stock_value'] = products['price'] * products['stock']
print("✓ 제품 재고 가치 계산 완료")

# 12.3 필터링
print("\n[3단계] 데이터 필터링")
top_students = students[students['average'] >= 85]
low_stock_products = products[products['stock'] < 30]
print(f"✓ 우수 학생: {len(top_students)}명")
print(f"✓ 저재고 제품: {len(low_stock_products)}개")

# 12.4 저장
print("\n[4단계] 결과 저장")
with pd.ExcelWriter('data/analysis_report.xlsx', engine='openpyxl') as writer:
    top_students.to_excel(writer, sheet_name='우수학생', index=False)
    low_stock_products.to_excel(writer, sheet_name='저재고제품', index=False)
print("✓ analysis_report.xlsx 저장 완료")


print("\n" + "=" * 60)
print("13. 실전 예제 2: 매출 데이터 분석")
print("=" * 60)

# 13.1 매출 데이터 읽기
df_sales = pd.read_csv('data/sales_2024.csv', 
                       parse_dates=['date'],
                       encoding='utf-8-sig')
print("\n매출 데이터:")
print(df_sales.head())
print(f"데이터 기간: {df_sales['date'].min()} ~ {df_sales['date'].max()}")

# 13.2 월별 집계
df_sales['year_month'] = df_sales['date'].dt.to_period('M')
monthly_sales = df_sales.groupby('year_month').agg({
    'sales_amount': 'sum',
    'customer_count': 'sum'
}).reset_index()
monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)

print("\n월별 매출:")
print(monthly_sales.head())

# 13.3 지역별 집계
region_sales = df_sales.groupby('region').agg({
    'sales_amount': ['sum', 'mean', 'count'],
    'customer_count': 'sum'
}).reset_index()
region_sales.columns = ['region', 'total_sales', 'avg_sales', 'transaction_count', 'total_customers']

print("\n지역별 매출:")
print(region_sales)

# 13.4 결과 저장
with pd.ExcelWriter('data/sales_analysis.xlsx', engine='openpyxl') as writer:
    monthly_sales.to_excel(writer, sheet_name='월별매출', index=False)
    region_sales.to_excel(writer, sheet_name='지역별매출', index=False)
print("\n✓ sales_analysis.xlsx 저장 완료")


print("\n" + "=" * 60)
print("14. 대용량 데이터 처리 (청크 방식)")
print("=" * 60)

# 14.1 청크 단위로 읽기 시뮬레이션
print("\n청크 단위 읽기:")
chunk_size = 100
chunk_count = 0
total_rows = 0

for chunk in pd.read_csv('data/sales_2024.csv', 
                         chunksize=chunk_size,
                         encoding='utf-8-sig'):
    chunk_count += 1
    total_rows += len(chunk)
    if chunk_count <= 3:  # 처음 3개 청크만 출력
        print(f"청크 {chunk_count}: {len(chunk)}행")

print(f"\n총 청크 수: {chunk_count}")
print(f"총 행 수: {total_rows}")


print("\n" + "=" * 60)
print("15. 파일 존재 확인 및 안전한 읽기")
print("=" * 60)

def safe_read_csv(filename):
    """안전하게 CSV 파일 읽기"""
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename, encoding='utf-8-sig')
            print(f"✓ {filename} 읽기 성공: {df.shape}")
            return df
        except Exception as e:
            print(f"✗ {filename} 읽기 실패: {e}")
            return None
    else:
        print(f"✗ {filename} 파일이 존재하지 않습니다.")
        return None

# 테스트
df_test1 = safe_read_csv('data/students.csv')
df_test2 = safe_read_csv('data/nonexistent.csv')


print("\n" + "=" * 60)
print("16. 데이터 백업 및 복원")
print("=" * 60)

# 16.1 Pickle로 저장 (가장 빠름)
df_students.to_pickle('data/students_backup.pkl')
print("\n✓ students_backup.pkl 저장 완료 (Pickle)")

# 16.2 Pickle에서 읽기
df_restored = pd.read_pickle('data/students_backup.pkl')
print(f"✓ Pickle에서 복원: {df_restored.shape}")
print("복원된 데이터:")
print(df_restored.head(3))


print("\n" + "=" * 60)
print("17. 생성된 출력 파일 목록")
print("=" * 60)

output_files = [
    'output_basic.csv',
    'output_selected.csv',
    'output_semicolon.csv',
    'output_students.xlsx',
    'output_multi_sheet.xlsx',
    'output_customers.json',
    'output_records.json',
    'output_index.json',
    'new_database.db',
    'orders_2024_all.csv',
    'cleaned_data.csv',
    'analysis_report.xlsx',
    'sales_analysis.xlsx',
    'students_backup.pkl'
]

print("\n생성된 파일:")
for file in output_files:
    filepath = f'data/{file}'
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✓ {file} ({size:,} bytes)")


print("\n" + "=" * 60)
print("데이터 로드 및 저장 실습 완료!")
print("=" * 60)

print("\n주요 학습 내용:")
print("  1. CSV 읽기/쓰기 (다양한 옵션)")
print("  2. Excel 읽기/쓰기 (여러 시트)")
print("  3. JSON 읽기/쓰기")
print("  4. SQLite 데이터베이스 연동")
print("  5. 여러 파일 병합")
print("  6. 결측치 처리")
print("  7. ETL 파이프라인 구현")
print("  8. 대용량 데이터 처리 (청크)")
