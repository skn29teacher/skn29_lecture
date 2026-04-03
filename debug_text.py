def calculate_average(scores):
    '''학생들의 점수를 받아 평균을 계산'''
    total = 0
    count = 0
    for score in scores:
        total += score
        count += 1
    if count == 0:
        return 0
    avg = total / count
    return avg
def process_student_data():
    '''학생들의 데이터를 읽어와 개별 평균을 반환'''
    students = {
        'Alice' : [80,90,100],
        'Bob':[70,85],
        'Charlie' : [88,98]
    }
    results = {}
    for name, scores in students.items():
        avg_score = calculate_average(scores)
        results[name] = avg_score
    return results

if __name__ == '__main__':
    final_grades =  process_student_data()
    print(f'[처리완료] 최종 결과')
    print(final_grades)