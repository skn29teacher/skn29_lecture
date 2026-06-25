import json

file_path = r'C:\Users\Playdata\Documents\20260605\Step2_Finetuning\RunPod_Finetuning_KoAlpaca.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# The target cell is cell index 6
cell_6_source = "".join(d['cells'][6]['source'])

# Replace the 2000 slice with the full dataset map
cell_6_source = cell_6_source.replace(
    'train_dataset = dataset.select(range(2000)).map(format_prompt)',
    'train_dataset = dataset.map(format_prompt)'
)
cell_6_source = cell_6_source.replace(
    '# 실습 시간을 위해 2,000개 데이터만 슬라이싱하여 프롬프트 적용',
    '# 전체 데이터를 사용하여 프롬프트 적용'
)
# Alternative comment text just in case the wording was slightly different:
cell_6_source = cell_6_source.replace(
    '# 실습 시간을 줄이기 위해 2,000개 데이터만 슬라이싱하여 프롬프트 적용',
    '# 전체 데이터를 사용하여 프롬프트 적용'
)

# Put it back as a list of strings
d['cells'][6]['source'] = [line + '\n' for line in cell_6_source.split('\n')]
# Fix last newline
if d['cells'][6]['source']:
    d['cells'][6]['source'][-1] = d['cells'][6]['source'][-1].rstrip('\n')

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=1)

print("Successfully updated cell 6 for full dataset mapping.")
