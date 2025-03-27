# Data Battle 2025
Par Carriac Simon, Khadija Bourrich, Mohammed Reda Belcadi abbassi, Mohamed Ilyas Abbana Bennani et Crahay--Boudou Florent
## Lancer l'application
Pour lancer le projet : 
Une fois a la racine du projet, taper dans le terminal : <br>
```docker build -t databattle .```<br>
```docker run -p 8000:80 -it databattle```<br>
Sur un navigateur, charger la page localhost:8000
<br><br>
Si vous souhaitez relancer le script python afin de rajouter des questions : il faut export une clé API Hugging Face sur votre terminal `export HF_TOKEN= "votre clé"` avec assez de crédits, executer le script text_to_json.py et enfin merge_json.py.

