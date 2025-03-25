import glob
import re
import json

def parse_question_block(block):
    """
    Extrait les différentes parties d'une question depuis un bloc de texte.
    Le bloc est censé contenir :
      - La ligne "Question X:" suivie du texte de la question
      - Les propositions de réponses débutant par "A)", "B)", "C)", "D)"
      - Une ligne "Correct answer:" indiquant la bonne option
      - Une section "Explanation:" pour la justification
      - Une éventuelle ligne "Source:" pour la référence
    """
    # Initialisation du dictionnaire avec les clés attendues
    qdict = {
        "question_number": None,
        "question_text": "",
        "answer_choices": {},
        "answer": "",
        "answer justification": "",
        "source": "",
        "type": "qcm"
    }

    # Extraction du texte de la question (entre "Question X:" et la première réponse commençant par une lettre)
    qtext_match = re.search(r'Question\s+\d+\s*:\s*(.*?)(?=\n\s*[A-D]\))', block, re.DOTALL | re.IGNORECASE)
    if qtext_match:
        qdict["question_text"] = qtext_match.group(1).strip()

    # Extraction des propositions de réponse (A) à D))
    # On capture la lettre et le texte correspondant sur une même ligne
    choices = re.findall(r'([A-D])\)\s*(.*)', block)
    for letter, text in choices:
        qdict["answer_choices"][letter.lower()] = text.strip()

    # Extraction de la bonne réponse (on attend "Correct answer:" suivi d'une lettre)
    answer_match = re.search(r'Correct answer\s*:\s*([A-D])', block, re.IGNORECASE)
    if answer_match:
        qdict["answer"] = answer_match.group(1).upper()

    # Extraction de la justification de la réponse (après "Explanation:")
    expl_match = re.search(r'Explanation\s*:\s*(.*?)(?=\n(?:Source\s*:|$))', block, re.DOTALL | re.IGNORECASE)
    if expl_match:
        qdict["answer justification"] = expl_match.group(1).strip()

    # Extraction de la source si présente (ligne commençant par "Source:")
    source_match = re.search(r'Source\s*:\s*(.*)', block, re.IGNORECASE)
    if source_match:
        qdict["source"] = source_match.group(1).strip()

    return qdict

def main():
    # Récupère tous les fichiers dont le nom commence par "quiz_output" et se termine par ".txt"
    files = glob.glob("../Data/generated _txt_questions/quiz_output*.txt")
    all_questions = []
    question_number = 1

    for filename in sorted(files):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # On découpe le contenu en blocs correspondant à chaque question.
        # Ici, on suppose que chaque question est précédée d'une ligne délimitée comme :
        # --- Question X (Chunk ...) ---
        blocks = re.split(r'\n-{3,}\s*Question\s+\d+.*?-{3,}\n', content)
        # Le premier bloc peut être l'en-tête, on le saute s'il ne contient pas de "Question"
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            # On vérifie qu'il y a bien une partie "Question" dans le bloc
            if "Question" not in block:
                continue
            # Analyse du bloc pour en extraire les données
            qdata = parse_question_block(block)
            qdata["question_number"] = question_number
            all_questions.append(qdata)
            question_number += 1

    # Optionnel : vérifier que l'on a bien 330 questions
    print(f"Nombre total de questions extraites : {len(all_questions)}")

    # Enregistrement dans un fichier JSON
    with open("../Data/generated_json_questions/questions_output.json", "w", encoding="utf-8") as out_file:
        json.dump(all_questions, out_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
