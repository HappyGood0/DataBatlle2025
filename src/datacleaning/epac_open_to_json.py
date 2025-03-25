import re
import json

with open(r'Data\EPAC_Exams txt\MOCK1 - mock_open_en.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by main question numbers (1\n, 2\n, etc.)
main_blocks = re.findall(r'(?:^|\n)([1-5])\.\s([\s\S]*?)(?=\n[1-5]\.\s|\Z)', text)



print(f"Total Blocks Found: {len(main_blocks)}")

dataset = []

for num, block in main_blocks:
    print(f"----- BLOCK {num} START -----")
    print(block[:300])
    print("----- BLOCK END -----\n")

    # Check for sub-questions like Q1-1, Q2-2
    sub_questions = re.findall(r'Q\d+-\d+\s+(.*?)(?=\nQ\d+-\d+|\Z)', block, re.DOTALL)

    if sub_questions:
        # Context is everything before first sub-question
        context_split = re.split(r'Q\d+-\d+\s+', block, maxsplit=1)
        context_text = context_split[0].strip().replace('\n', ' ')

        questions_list = []
        for q_idx, q_text in enumerate(sub_questions, 1):
            questions_list.append({
                "question_number": q_idx,
                "question_text": q_text.strip().replace('\n', ' ')
            })

        dataset.append({
            "question_number": int(num),
            "context": context_text,
            "questions": questions_list,
            "type": "open"
        })
    else:
        # If no sub-questions, treat last sentence as question
        sentences = re.split(r'(\.|\?|!)\s+', block.strip())
        if len(sentences) >= 2:
            context_text = ' '.join(sentences[:-2]).replace('\n', ' ') + sentences[-2]
            question_text = sentences[-1]
        else:
            context_text = block.strip().replace('\n', ' ')
            question_text = ""

        dataset.append({
            "question_number": int(num),
            "context": context_text,
            "questions": [{
                "question_number": 1,
                "question_text": question_text.strip()
            }],
            "type": "open"
        })

# Final JSON is a list of question objects (no global number_of_main_questions field)
final_output = dataset

# Save to JSON
output_path = r'Data\EPAC_Exams JSON\MOCK1_open_dataset.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(final_output, json_file, indent=4, ensure_ascii=False)

print("✅ MOCK Final Open Questions JSON Generated Successfully!")
