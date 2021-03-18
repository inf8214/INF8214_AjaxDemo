import json, re
from   flask      import Flask, render_template, request, send_file, jsonify
from   pathlib    import Path
from   flask_cors import CORS # Important si serveur Flask sur la même machine qu'un autre serveur!!


# Setup Flask app.
app = Flask(__name__)
# app.config['SERVER_NAME'] = ''
# app.config['APPLICATION_ROOT'] = ''
CORS(app)


# Routes
####################################

# Route racine
@app.route('/')
def index():
    # Retourne html à partir d'un template
    return render_template('index.html')

# Route spécifique sans paramètres
@app.route('/allo')
def allo():
    # Retourne html directement
    return "<h1>Allo!</h1>"

# Route spécifique avec paramètres dans le chemin d'accès
@app.route('/allo/<nom>')
def allo_nom(nom):
    # Retourne html à partir d'un template en passant un paramètre
    return render_template('allo.html', nom=nom)

# Route spécifique avec paramètres comme arguments nommés
@app.route('/bonjour')
def bonjour():
    prenom = request.args.get('prenom')
    nom    = request.args.get('nom')
    # Retourne html directement, avec interpolation
    return f"<h1>Bonjour {prenom} {nom}!</h1>"

# Route pour liste des photos en html, à partir d'un json local
@app.route('/liste')
def liste():
    # Fichier json local
    filepath = './static/json/img.json'
    with open(filepath, 'r') as f:
        data = f.read()
    # Liste de dictionnaire
    images = json.loads(data)
    # Retourne html à partir d'un template en passant des paramètres issus d'un fichier json
    return render_template('liste.html', images=images)

# Route pour liste des photos en json, à partir d'un json local, filtré par argument nommé
@app.route('/listeJson')
def listeJson():
    # Fichier json local
    filepath = './static/json/img.json'
    with open(filepath, 'r') as f:
        data = f.read()
    # Liste de dictionnaire
    images = json.loads(data)
    # Filtrer les images
    if request.args.get('droits'):
        droits = True if request.args.get('droits').capitalize() == "True" else False
        images = list(filter(lambda image: image['droits']==droits, images))
    # Retourne json
    return jsonify(images)

# Route pour demo du 18 mars
@app.route('/imageList')
def listeJson():
    filepath = './static/json/imageList.json'
    with open(filepath, 'r') as f:
        data = f.read()
    images = json.loads(data)
    if request.args.get('droits'):
        droits = True if request.args.get('droits').capitalize() == "True" else False
        images = list(filter(lambda image: image['droits']==droits, images))
    return jsonify(images)

# Route pour chemin d'accès complet vers ressource/fichier
@app.route('/<path:path>')
def fichier(path):
    # Retourne fichier static
    return app.send_static_file(path)



# Diseabling caching
####################################
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# Run Flask!
###################################
if __name__ == '__main__':
    app.run(debug=True)
