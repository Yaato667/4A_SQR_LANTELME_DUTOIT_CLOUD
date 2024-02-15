from flask import Flask, request, jsonify, abort
import redis

app = Flask(__name__)

# Connexion à Redis sur localhost
redis_conn = redis.Redis()

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

    return jsonify({"resultat": resultat})

# Route pour soustraire deux nombres
@app.route('/api/soustraction', methods=['POST'])
def soustraction():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("soustraction", nb1, nb2)

    return jsonify({"resultat": resultat})

# Route pour multiplier deux nombres
@app.route('/api/multiplication', methods=['POST'])
def multiplication():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("multiplication", nb1, nb2)

    return jsonify({"resultat": resultat})

# Route pour diviser deux nombres
@app.route('/api/division', methods=['POST'])
def division():
    data = request.get_json()
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not nb1 or not nb2:
        abort(400, "Valeurs manquantes")

    resultat = effectuer_calcul("division", nb1, nb2)

    return jsonify({"resultat": resultat})

# Route pour récupérer le résultat d'un calcul
@app.route('/api/result/<int:id_resultat>', methods=['GET'])
def get_resultat(id_resultat):
    if id_resultat <= 0:
        abort(400, "ID invalide")

    # Vérifier si le résultat est déjà stocké dans Redis
    resultat_str = redis_conn.get("resultat_" + str(id_resultat))

    # Si le résultat est trouvé dans Redis, le décoder et le retourner
    if resultat_str:
        return jsonify({"resultat": int(resultat_str)})

    # Si le résultat n'est pas trouvé dans Redis, renvoyer une erreur
    abort(404, "Résultat non trouvé")

if __name__ == '__main__':
    app.run(debug=True)