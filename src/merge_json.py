import json
import os

files = []

json_dirs = [
    "../Data/EPAC_EXAMS FINAL DATASET/MCQ",
    "../Data/EPAC_EXAMS FINAL DATASET/OPEN",
    "../Data/EQE_Exams/01-Pre-Examen-json",
    "../Data/generated_json_questions"
]

for json_dir in json_dirs:
    for filename in os.listdir(json_dir):
        if filename.lower().endswith(".json"):
            files.append(os.path.join(json_dir, filename))

liste = []

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        liste.extend(data)

to_delete = []

for i, data in enumerate(liste):
    data.pop("question_number", None)  # ✅ pas d'erreur si la clé n'existe pas

    # Supprimer les objets qui ne sont pas de type QCM
    if "questions" in data or ("type" in data and data["type"] == "open"):
        to_delete.append(i)

# Suppression en ordre inverse
for i in reversed(to_delete):
    liste.pop(i)

# Enregistrement du JSON fusionné
output_path = '../Data/many_to_one.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(liste, json_file, indent=4, ensure_ascii=False)

print("✅ JSON merge successful! ✅")
