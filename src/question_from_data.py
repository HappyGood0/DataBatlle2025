import json
import os

files = []

json_dir = "Data/EPAC_Exams JSON"

for filename in os.listdir(json_dir):
    if filename.lower().endswith(".json"):
        files.append(json_dir+"/"+filename)

liste = []

for file in files :
    # Opening JSON file

    f = open(file)

    # returns JSON object as a dictionary and add this item in somme 
    data =  json.load(f)
    
    liste.extend(data)

    # Closing file
    f.close()

#liste contiendra une liste de toute les questions référencée 