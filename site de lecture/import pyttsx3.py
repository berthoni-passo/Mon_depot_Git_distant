import os
import pyttsx3
import PyPDF2
import docx2txt
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def lire_document(chemin_fichier):
    passo = pyttsx3.init()  # Créez une nouvelle instance de l'objet pyttsx3 pour chaque lecture

    if chemin_fichier.endswith('.pdf'):
        lecture = PyPDF2.PdfReader(chemin_fichier)
        for page_number in range(len(lecture.pages)):
            page = lecture.pages[page_number]
            texte = page.extract_text()
            passo.say(texte)
            passo.runAndWait()

    elif chemin_fichier.endswith('.docx'):
        texte = docx2txt.process(chemin_fichier)
        passo.say(texte)
        passo.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lire', methods=['POST'])
def lire():
    if 'file' in request.files:
        fichier = request.files['file']
        if fichier.filename != '':
            # Enregistrez le fichier téléchargé dans le répertoire temporaire
            chemin_temporaire = os.path.join('temp', fichier.filename)
            fichier.save(chemin_temporaire)

            # Lire le document depuis le répertoire temporaire
            lire_document(chemin_temporaire)

            # Supprimez le fichier temporaire après la lecture
            os.remove(chemin_temporaire)

            return render_template('resultat.html', message="Document lu avec succès.")
    return render_template('resultat.html', message="Aucun fichier sélectionné ou une erreur s'est produite.")

@app.route('/saluer', methods=['POST'])
def saluer():
    data = request.get_json()
    nom_utilisateur = data.get('nomUtilisateur', '')

    # Utilisez la voix pour saluer l'utilisateur
    passo = pyttsx3.init()  # Créez une nouvelle instance de l'objet pyttsx3
    passo.say(f"Bonjour {nom_utilisateur}, je suis un droid de la troisième génération conçu par Passo pour vous assister dans vos tâches. Alors, installez-vous confortablement.")
    passo.runAndWait()

    return jsonify({"message": f"Bienvenue, {nom_utilisateur}!"})

if __name__ == '__main__':
    # Assurez-vous que le dossier temporaire existe
    os.makedirs('temp', exist_ok=True)

    # Ajoutez le dossier statique pour servir les images de fond
    app.config['STATIC_FOLDER'] = 'static'

    app.run(debug=True)
