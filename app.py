from flask import *
import os
from src.fractal import salva_immagine_felce

app=Flask(__name__) #da il nominativo all' app in questo caso parte se è _main_ quindi solo dal file sorgente

@app.route('/')
def home ():
    return render_template('index.html')

@app.route('/generate', methods=["GET", "POST"])
def generate():
    if request.method == "GET":
        return render_template('generate.html')

    nome = request.form["nome"] 
    n_punti = int(request.form["n_punti"])
    color = request.form["color"]
    face_color = request.form["face_color"]

    # Salviamo il percorso relativo restituito dalla funzione
    path_relativo = salva_immagine_felce(nome, n_punti, color, face_color)

    # Passiamo 'image' al template perché in HTML usi {{ image }}
    return render_template('generate.html', image=path_relativo)


@app.route('/archive')
def archive():
    # Percorso della cartella contenente le immagini
    # Usiamo un percorso relativo alla cartella 'static'
    folder_path = os.path.join('static', 'frattali_img')
    
    # Verifichiamo se la cartella esiste, altrimenti creiamo una lista vuota
    if os.path.exists(folder_path):
        # Elenca tutti i file nella cartella
        files = os.listdir(folder_path)
        # Filtriamo per sicurezza solo i file .png
        immagini = [f for f in files if f.endswith('.png')]
        # Ordiniamo le immagini (opzionale, magari dalla più recente)
        immagini.sort(reverse=True)
    else:
        immagini = []

    return render_template('archive.html', immagini=immagini)

@app.route('/info')
def info():
    return render_template('info_felce.html')

if __name__  =='__main__':
    app.run(debug=True)
