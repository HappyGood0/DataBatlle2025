import re
import json

with open(r'Data\\EPAC_Exams txt\\2023 - EPAC_solution_mcq.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by Question blocks like 'Question 1:'
question_blocks = re.findall(r'(Question \d+\s*:\s*[A-D])([\s\S]*?)(?=Question \d+\s*:\s*[A-D]|\Z)', text)

dataset = []

for block in question_blocks:
    answer_match = re.match(r'Question (\d+)\s*:\s*([A-D])', block[0].strip())
    if not answer_match:
        continue
    question_num, answer_letter = answer_match.groups()

    # Extract explanation text up to the keyword 'Legal basis' (not including 'Legal basis')
    legal_basis_split = re.search(r'Legal basis\s*', block[1], flags=re.IGNORECASE)
    if legal_basis_split:
        explanation_part = block[1][:legal_basis_split.start()].strip().replace('\n', ' ')
        legal_part = block[1][legal_basis_split.end():].strip()
    else:
        explanation_part = None  # If explanation missing, set to None
        legal_part = block[1].strip()

    print(f"Question {question_num} detected, Answer: {answer_letter}")
    print("Explanation Sample:", explanation_part[:100] if explanation_part else "No Explanation")

    # Process legal_part line by line instead of splitting by double newlines
    sections = legal_part.strip().splitlines()

    legal_basis = []
    for section in sections:
        section = section.strip()

        # Skip separator lines like dashes or underscores
        if re.match(r'^\s*[-_]{5,}\s*$', section):
            continue

        # Skip page numbers (lines that are only digits)
        if re.match(r'^\s*\d+\s*$', section):
            continue

        if section.startswith("Rule") or section.startswith("Decision") or section.startswith("Article"):
            legal_basis.append({
                "type": "rule",
                "rule": section,
                "rule_text": ""
            })
        else:
            legal_basis.append({
                "type": "other",
                "text": section.replace('\n', ' ')
            })

    dataset.append({
        "question_number": int(question_num),
        "answer": answer_letter,
        "explanation": explanation_part if explanation_part else None,
        "legal_basis": legal_basis
    })

# Save as JSON
output_path = r'Data\\EPAC_Exams JSON\\2023_EPAC_mcq_answers.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(dataset, json_file, indent=4, ensure_ascii=False)

print("✅ 2023 MCQ Answers JSON Generated Successfully!")
