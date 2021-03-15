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

# Racine
@app.route('/')
def index():
    # Retourne html à partir d'un template
    return render_template('index.html')

# Route spécifique sans paramètres
@app.route('/allo')
def allo():
    # Retourne html directement
    return "<h1>Allo!</h1>"

# Route spécifique avec paramètres
@app.route('/allo/<nom>')
def allo_nom(nom):
    # Retourne html à partir d'un template en passant un paramètre
    return render_template('allo.html', nom=nom)

# Chemin d'accès complet
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
