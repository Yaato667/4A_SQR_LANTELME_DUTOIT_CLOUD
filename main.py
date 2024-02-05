from flask import Flask, request, jsonify, abort
import math

app = Flask(__name__)

# Liste pour stocker les résultats
resultats = []

# Fonction pour effectuer le calcul
def effectuer_calcul(operation, nb1, nb2):
    if operation == "addition":
        return nb1 + nb2
    elif operation == "soustraction":
        return nb1 - nb2
    elif operation == "multiplication":
        return nb1 * nb2
    elif operation == "division":
        if nb2 == 0:
            abort(400, "Division par zéro impossible")
        return nb1 / nb2
    else:
        abort(400, "Opération inconnue")

# Route pour additionner deux nombres
@app.route('/api/addition', methods=['POST'])
def addition():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("addition", nb1, nb2)
    id_resultat = len(resultats) + 1
    resultats.append(resultat)

    return jsonify({"id": id_resultat})

# Route pour soustraire deux nombres
@app.route('/api/soustraction', methods=['POST'])
def soustraction():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("soustraction", nb1, nb2)
    id_resultat = len(resultats) + 1
    resultats.append(resultat)

    return jsonify({"id": id_resultat})

# Route pour multiplier deux nombres
@app.route('/api/multiplication', methods=['POST'])
def multiplication():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("multiplication", nb1, nb2)
    id_resultat = len(resultats) + 1
    resultats.append(resultat)

    return jsonify({"id": id_resultat})

# Route pour diviser deux nombres
@app.route('/api/division', methods=['POST'])
def division():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("division", nb1, nb2)
    id_resultat = len(resultats) + 1
    resultats.append(resultat)

    return jsonify({"id": id_resultat})

# Route pour récupérer le résultat d'un calcul
@app.route('/api/result/<int:id_resultat>', methods=['GET'])
def get_resultat(id_resultat):
    if id_resultat <= 0 or id_resultat > len(resultats):
        abort(404, "Résultat introuvable")

    resultat = resultats[id_resultat - 1]
    return jsonify({"resultat": resultat})

if __name__ == '__main__':
    app.run(debug=True)