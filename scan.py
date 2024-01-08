from flask import Flask, request, jsonify
from PIL import Image
from pyzbar.pyzbar import decode
from flask_cors import CORS
import io
import base64


app = Flask(__name__)
CORS(app)

@app.route('/scan', methods=['POST'])
def scanner_code_barre():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'erreur': 'Aucune image envoyée'}), 400

    image_data = data['image'].split(',')[1]  # Ignore le préfixe "data:image/jpeg;base64,"
    image_bytes = bytearray(image_data, 'utf-8')

    try:
        # Convertir les données de l'image en format Image
        img = Image.open(io.BytesIO(base64.b64decode(image_bytes)))

        # Décoder le code-barres
        codes_barres = decode(img)

        # Récupérer les données du code-barres
        resultats = []
        for code_barre in codes_barres:
            data = code_barre.data.decode('utf-8')
            resultats.append(data)

        return jsonify({'resultats': resultats})

    except Exception as e:
        return jsonify({'erreur': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
