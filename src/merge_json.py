import json
import os

files = []

json_dirs = ["Data/EPAC_EXAMS FINAL DATASET/MCQ", "Data/EPAC_EXAMS FINAL DATASET/OPEN", "Data/EQE_Exams/01-Pre-Examen-json"]


for json_dir in json_dirs:
    for filename in os.listdir(json_dir):
        if filename.lower().endswith(".json"):
            files.append(json_dir+"/"+filename)

liste = []

for file in files :
    # Opening JSON file
    f = open(file)

    data = json.load(f)
    
    liste.extend(data)

    f.close()

to_delete = []

for i, data in enumerate(liste):
    data.pop("question_number")
    if "questions" in data and ("type" not in data or data["type"] != "open") :
        data.update({"type" : "open"})

for i in range(len(to_delete)-1, -1, -1):
    liste.pop(to_delete[i])


# Save JSON
output_path = 'Data/many_to_one.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(liste, json_file, indent=4, ensure_ascii=False)

print("JSON merge Successfully!")