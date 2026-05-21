import json
import random
from pathlib import Path

LABEL_DESC = {
    'DEF': '정의/목적/적용범위 조항',
    'RIGHT': '권리/의무/금지/책임 조항',
    'PROC': '신청/심사/조사/불복/처벌 절차 조항',
    'ORG': '기관/위원회/법원 등 조직의 설치/구성/권한 조항',
    'CRIT': '자격/요건/기준/기간/수치 조건 조항',
    'ETC': '시행일/경과조치/위임 등 기타 조항',
}

TEMPLATES = {
    'DEF': [
        '이 규정에서 사용되는 용어의 정의는 다음과 같다: {term}은 {definition}을 말한다.',
        '{term}의 목적은 {purpose}에 있으며, 적용범위는 {scope}로 한다.',
    ],
    'RIGHT': [
        '사용자는 {action}할 권리를 가지며, 다음과 같은 의무를 진다: {duty}.',
        '사업자는 {prohibition}을 금지하며, 위반 시 {penalty}의 책임을 진다.',
    ],
    'PROC': [
        '신청은 {who}에게 제출하며, 심사는 {period} 이내에 완료한다.',
        '불복 절차는 {procedure}에 따라 진행되며, 이의신청은 {deadline}까지 가능하다.',
    ],
    'ORG': [
        '위원회는 {members}로 구성되며, 위원회의 권한은 {authority}로 한다.',
        '{org}를 설치하여 {task}를 수행한다.',
    ],
    'CRIT': [
        '응시자는 {qualification}을 갖추어야 하며, 자격 유효기간은 {period}이다.',
        '선정 기준은 {criteria}이며, 최소 점수는 {score} 이상으로 한다.',
    ],
    'ETC': [
        '이 규정은 {effective_date}부터 시행한다.',
        '경과조치는 {transition}에 따른다.',
    ],
}


def random_phrase(key):
    if key == 'term':
        return random.choice(['계약', '서비스', '회원'])
    if key == 'definition':
        return random.choice(['특정한 의미', '시스템 사용을 위한 조건', '이 문서에서 정의한 바'])
    if key == 'purpose':
        return random.choice(['공정한 운영', '안전한 서비스 제공', '정보 보호'])
    if key == 'scope':
        return random.choice(['국내 전역', '회원에게만', '모든 이용자에게'])
    if key == 'action':
        return random.choice(['정보 열람', '서비스 이용', '데이터 수정'])
    if key == 'duty':
        return random.choice(['정확한 정보 제공', '비밀번호 관리', '법령 준수'])
    if key == 'prohibition':
        return random.choice(['무단 복제', '부정 이용', '스팸 발송'])
    if key == 'penalty':
        return random.choice(['손해배상', '서비스 중지', '과태료'])
    if key == 'who':
        return random.choice(['관리자', '담당부서', '접수처'])
    if key == 'period':
        return random.choice(['14일', '30일', '60일'])
    if key == 'procedure':
        return random.choice(['서면 제출', '온라인 접수', '심사위원회 회부'])
    if key == 'deadline':
        return random.choice(['7일', '14일', '30일'])
    if key == 'members':
        return random.choice(['5인 이상', '위원장 포함 7인', '관련 전문가로 구성'])
    if key == 'authority':
        return random.choice(['결정권', '조정권', '심사권'])
    if key == 'org':
        return random.choice(['조정위원회', '전담부서'])
    if key == 'task':
        return random.choice(['심사', '집행', '감독'])
    if key == 'qualification':
        return random.choice(['학위 취득자', '관련 경력 3년 이상', '자격증 보유자'])
    if key == 'criteria':
        return random.choice(['성적', '경력', '면접 점수'])
    if key == 'score':
        return random.choice(['70', '80', '85'])
    if key == 'effective_date':
        return random.choice(['2026-01-01', '2026-06-01', '2026-12-01'])
    if key == 'transition':
        return random.choice(['종전 규정 준수', '유예 기간 6개월'])
    return '...'


def synthesize_clause(label):
    tpl = random.choice(TEMPLATES[label])
    # replace placeholders
    while '{' in tpl:
        start = tpl.find('{')
        end = tpl.find('}', start)
        key = tpl[start+1:end]
        tpl = tpl[:start] + random_phrase(key) + tpl[end+1:]
    return tpl


def make_prompt(clause):
    labels = ', '.join([f"{k}({v})" for k, v in LABEL_DESC.items()])
    prompt = (
        f"다음 조항을 다음 라벨 중 하나로 분류하시오. 가능한 라벨: {labels}\n"
        f"조항: {clause}\n라벨:"
    )
    return prompt


def generate(out_dir='./finetune_data', train_size=2000, val_size=400, seed=42):
    random.seed(seed)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    def write_file(path, n):
        with open(path, 'w', encoding='utf-8') as f:
            for _ in range(n):
                label = random.choice(list(LABEL_DESC.keys()))
                clause = synthesize_clause(label)
                prompt = make_prompt(clause)
                item = {'prompt': prompt, 'response': label}
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    write_file(out / 'train.jsonl', train_size)
    write_file(out / 'validation.jsonl', val_size)
    print(f'Wrote train/validation to {out.resolve()}')


if __name__ == '__main__':
    generate()
