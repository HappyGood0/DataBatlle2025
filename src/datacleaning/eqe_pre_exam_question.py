import re
import json

with open('Data/EQE_Exams/01-Pre-Examen-txt/2021_PreEx_questions_EN.txt', 'r', encoding='utf-8') as f:
    text = f.read()
f.close()

# Regex to split the full text by question numbers
question_blocks = re.findall(r'Question [0-9]+.*?(?=Question [0-9]+|$)', text, re.DOTALL)

dataset = []

for idx, block in enumerate(question_blocks, 1):
    if idx > 10:
        break;
    question_part, answer_part = re.split(r'For each of the statements.*?is true or false:', block, maxsplit=1, flags=re.DOTALL)

    # Clean the question text
    question_text = re.sub(r'Question [0-9]+[ ]*', '', question_part.strip().replace('\n', ' '))

    # Now extract answer choices dynamically (A. B. C. D. etc.)
    answers = re.findall(r'[0-9]+\.[0-9]+.*?(?=[0-9]+\.[0-9]+|$)', answer_part, re.DOTALL)
    answer_choices = {re.sub(r'[0-9]+.', "", re.search(r'[0-9]+.[0-9]+', answer, re.DOTALL).group()) : re.sub(r' *\n', " ", re.sub(r'([0-9]+\.[0-9]+|2021/PE/EN)', '', answer)) for answer in answers}

    dataset.append({
        "question_number": idx,
        "question_text": question_text,
        "answer_choices": answer_choices,
        "type": "true or false"
    })

with open('Data/EQE_Exams/01-Pre-Examen-txt/2021_PreEx_answers_EN.txt', 'r', encoding='utf-8') as f:
    text = f.read()
f.close()

question_blocks = re.findall(r'(?:QUESTION|Question).*?(?=QUESTION|Question|$)', text, re.DOTALL)

for idx in range(len(dataset)):
    block = question_blocks[idx]

    question_part = re.split(r'[0-9]+\.[0-9]+ (?:-|–) (?:True|False|TRUE|FALSE)', block, maxsplit=1, flags=re.DOTALL)[0]

    # Clean the question text
    question_text = re.sub(r' *\n', " ", re.sub(r'(?:QUESTION|Question) [0-9]+[ ]*\n', '', question_part))

    answers = re.findall(r'([0-9]+\.[0-9]+ (?:-|–) (?:True|False|TRUE|FALSE))', block)
    answer_choices = {re.sub(r'[0-9]+.', "", re.search(r'[0-9]+.[0-9]+', answer, re.DOTALL).group()) : re.search(r'(True|False|TRUE|FALSE)', answer, re.DOTALL).group().capitalize() for answer in answers}

    dataset[idx].update({
        "answer_explanation": question_text,
        "answers": answer_choices
    })

# Save JSON
output_path = 'Data/EQE_Exams/01-Pre-Examen-json/2021_PreEx.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(dataset, json_file, indent=4, ensure_ascii=False)

print("JSON Generated Successfully!")
