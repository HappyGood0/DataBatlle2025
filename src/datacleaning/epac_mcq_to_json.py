import re
import json

with open(r'Data\EPAC_Exams txt\MOCK2 - mock_mcq_en.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Regex to split the full text by question numbers
question_blocks = re.findall(r'((?:1[0-5]|[1-9])\.\s[\s\S]*?)(?=\n(?:1[0-5]|[1-9])\.\s|\Z)', text)

dataset = []

for idx, block in enumerate(question_blocks, 1):
    # Only split if 'A.' exists
    if '\nA. ' in block:
        question_part, answer_part = re.split(r'\nA\.\s+', block, maxsplit=1)

        # Clean the question text
        question_text = question_part.strip().replace('\n', ' ')

        # Now extract answer choices dynamically (A. B. C. D. etc.)
        answers = re.findall(r'([A-Z])\.\s(.*?)(?=\n[A-Z]\.\s|\Z)', 'A. ' + answer_part, re.DOTALL)
        answer_choices = {letter.lower(): choice.strip().replace('\n', ' ') for letter, choice in answers}

        dataset.append({
            "question_number": idx,
            "question_text": question_text,
            "answer_choices": answer_choices,
            "type": "qcm"
        })
    else:
        print(f"Skipped block {idx}: 'A.' not found")


# Save JSON
output_path = r'Data\EPAC_Exams JSON\MOCK2_EPAC_mcq_dataset.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(dataset, json_file, indent=4, ensure_ascii=False)

print("JSON Generated Successfully!")
