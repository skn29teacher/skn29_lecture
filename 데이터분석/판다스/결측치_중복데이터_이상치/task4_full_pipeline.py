import pandas as pd
import numpy as np

def run_preprocessing_pipeline(file_path):
    '''file_path : csv 파일명'''
    # 데이터 로드
    try:
        df = pd.read_csv(file_path,encoding='utf-8')
    except UnicodeEncodeError as e:
        df = pd.read_csv(file_path,encoding='cp949')
    # 결측치 처리(대치)
    # age, salary는 중앙값으로 
    df['age'] = df['age'].fillna(df['age'].median())
    df['salary'] = df['salary'].fillna(df['salary'].median())
    # score 선형보간 하고 양끝에 남은 nan은 앞뒤 값으로 채움
    df['score'] = df['score'].interpolate(method='linear')
    df['score'] = df['score'].bfill().ffill()
    # 이상치 처리 capping(경계값으로 이상치를 대치)
    numeric_cols = ['age','salary','score']
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - IQR*1.5
        upper = Q3 + IQR*1.5
        df[col] = df[col].clip(lower=lower, upper=upper)
    # 중복데이터
    df = df.drop_duplicates(keep='first')
    # 종료
    print(f'파이프라인 종료')
    print(f'shape = {df.shape}')

if __name__ == "__main__":
    file_path = 'data/messy_data.csv'
    clean_df = run_preprocessing_pipeline(file_path)
    clean_df.to_csv('data/clean_data.csv',encording='utf-8')
    print('데이터 저장완료')   
