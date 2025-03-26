import re
import json

dataset = []
idx = 1

with open('Data/EQE_Exams/02-Paper-D-txt/2021_PaperD1-1_questions_EN.txt', 'r', encoding='utf-8') as f:
    text = f.read()
f.close()

# Regex to split the full text by question numbers
question_blocks = re.findall(r'QUESTION [0-9]+.*?(?=QUESTION [0-9]+|$)', text, re.DOTALL)

for block in question_blocks:

    question_text = re.sub(r'^[ ]*', '', re.sub(r'[ ]*\n', ' ', re.sub(r'(?:2021/D1-1/EN/1|\([0-9]+ MARKS\)|QUESTION [0-9]+)', '', block.strip())))

    dataset.append({
        "question_number": idx,
        "question_text": question_text,
        "type": "open"
    })
    idx+=1

with open('Data/EQE_Exams/02-Paper-D-txt/2021_PaperD1-2_questions_EN.txt', 'r', encoding='utf-8') as f:
    text = f.read()
f.close()

question_blocks = re.findall(r'QUESTION [0-9]+.*?(?=QUESTION [0-9]+|$)', text, re.DOTALL)

for block in question_blocks:

    question_text = re.sub(r'^[ ]*', '', re.sub(r'[ ]*\n', ' ', re.sub(r'(?:2021/D1-1/EN/1|\([0-9]+ MARKS\)|QUESTION [0-9]+)', '', block.strip())))

    dataset.append({
        "question_number": idx,
        "question_text": question_text,
        "type": "open"
    })
    idx+=1


with open('Data/EQE_Exams/02-Paper-D-txt/2021_PaperD_Candidate_answers.txt', 'r', encoding='utf-8') as f:
    text = f.read()
f.close()

question_blocks = re.findall(r'\n[0-9]+\.[ ]*\n.*?(?=\n[0-9]+\.[ ]*\n|$)', text, re.DOTALL)

for idx in range(len(dataset)):
    block = question_blocks[idx]

    question_part = re.sub(r'\n[0-9]+\.[ ]*\n', '', block).strip().replace('\n', ' ')

    dataset[idx].update({
        "answers": question_part
    })

print(dataset)

# Save JSON
output_path = 'Data/EQE_Exams/02-Paper-D-json/2021_Paper.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(dataset, json_file, indent=4, ensure_ascii=False)

print("JSON Generated Successfully!")
