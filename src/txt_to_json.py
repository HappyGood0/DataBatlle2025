import glob
import re
import json

def parse_question_block(block, q_number):
    qdict = {
        "question_text": f"{q_number}. ",
        "answer_choices": {},
        "type": "qcm",
        "answer": "",
        "explanation": None,
        "legal_basis": []
    }

    # Texte de la question
    qtext_match = re.search(r'Question\s+\d+\s*:\s*(.*?)(?=\n\s*[A-D]\))', block, re.DOTALL)
    if qtext_match:
        qdict["question_text"] += qtext_match.group(1).strip()
    else:
        print(f"❌ Question text not found in block {q_number}")
        return None

    # Choix de réponses
    choices = re.findall(r'([A-D])\)\s*(.*)', block)
    if not choices:
        print(f"❌ No choices found in block {q_number}")
        return None

    for letter, text in choices:
        qdict["answer_choices"][letter.lower()] = text.strip()

    # Bonne réponse
    answer_match = re.search(r'Correct answer\s*:\s*([A-D])', block, re.IGNORECASE)
    if answer_match:
        qdict["answer"] = answer_match.group(1).upper()
    else:
        print(f"❌ Correct answer not found in block {q_number}")
        return None

    # Explication
    expl_match = re.search(r'Explanation\s*:\s*(.*?)(?=\nSource\s*:|\n*$)', block, re.DOTALL | re.IGNORECASE)
    if expl_match:
        explanation = expl_match.group(1).strip()
        if explanation.lower() not in ["none", ""]:
            qdict["explanation"] = explanation

    # Base légale
    source_match = re.search(r'Source\s*:\s*(.*)', block, re.IGNORECASE)
    if source_match:
        source_text = source_match.group(1).strip()
        if source_text:
            qdict["legal_basis"].append({
                "type": "other",
                "text": source_text
            })

    return qdict

def main():
    files = glob.glob("../Data/generated _txt_questions/quiz_output_*.txt")
    all_questions = []
    question_number = 1

    for filename in sorted(files):
        print(f"📄 Lecture du fichier : {filename}")
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Séparation robuste des blocs
        blocks = re.split(r'-{3,}\s*Question\s+\d+\s*\(Chunk\s+\d+\)\s*-{3,}', content)
        print(f"📦 {len(blocks)} blocs trouvés")

        for block in blocks:
            block = block.strip()
            if not block or "Question" not in block:
                continue

            qdata = parse_question_block(block, question_number)
            if qdata:
                all_questions.append(qdata)
                question_number += 1

    print(f"\n✅ Total questions parsed: {len(all_questions)}")

    # Sauvegarde
    with open("../Data/generated_json_questions/questions_output.json", "w", encoding="utf-8") as out_file:
        json.dump(all_questions, out_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()

