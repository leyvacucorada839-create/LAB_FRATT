import matplotlib
matplotlib.use('Agg')  # Necessario per ambienti server/web
import matplotlib.pyplot as plt
import random
import os
import datetime
from map.db import add_mapping

# Parametri standard della Felce di Barnsley: (a, b, c, d, e, f, probabilità)
TRASFORMAZIONI = [
    (0.00,  0.00,  0.00,  0.16, 0.00, 0.00, 0.01), # Gambo
    (0.85,  0.04, -0.04,  0.85, 0.00, 1.60, 0.85), # Gruppi successivi
    (0.20, -0.26,  0.23,  0.22, 0.00, 1.60, 0.07), # Foglie SX
    (-0.15, 0.28,  0.26,  0.24, 0.00, 0.44, 0.07)  # Foglie DX
]

def applica_affine(x, y, t):
    """Calcola le coordinate successive usando la trasformazione affine"""
    a, b, c, d, e, f, _ = t
    x_new = a * x + b * y + e
    y_new = c * x + d * y + f
    return x_new, y_new

def genera_immagine_felce(n_punti=100000, colore='#32CD32', face_color='#000'):
    """
    Genera i punti del frattale e lo mostra su matplotlib.
    """
    x, y = 0.0, 0.0
    xs, ys = [], []
    
    pesi = [t[6] for t in TRASFORMAZIONI]
    
    for i in range(n_punti):
        t = random.choices(TRASFORMAZIONI, weights=pesi, k=1)[0]
        x, y = applica_affine(x, y, t)
        
        if i > 20:
            xs.append(x)
            ys.append(y)

    """plt.figure(figsize=(6, 10))
    plt.scatter(xs, ys, s=0.1, color=colore, marker='.')
    
    plt.axis('off')  # toglie assi per effetto "frattale pulito"
    plt.title("Felce di Barnsley", fontsize=12)"""

    fig=plt.figure(figsize=(6, 10), facecolor=face_color)
    plt.scatter(xs, ys, s=0.1, color=colore, marker='.')
    plt.axis('off')
    #plt.title("Felce di Barnsley", fontsize=12)

    return fig
    
    #plt.show()


def salva_immagine_felce(nome="felce", n_punti=100000, colore='#32CD32', face_color='#000'):
    fig = genera_immagine_felce(n_punti, colore, face_color)

    # Percorso reale su disco
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    output_dir = os.path.join(project_root, "static", "frattali_img")

    os.makedirs(output_dir, exist_ok=True)

    # Nome file
    filename = f"{nome}_{datetime.datetime.now().strftime('%Y-%m-%d')}.png"

    # Salvataggio su disco
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close(fig)

    print("Salvata in:", filepath)

    params={
        "n_punti": n_punti,
        "colore": colore,
        "face_color": face_color,
    }

    add_mapping(nome, 0, params)

    
    #IMPORTANTE: ritorna path RELATIVO a static
    relative_path = f"frattali_img/{filename}"
    return relative_path
