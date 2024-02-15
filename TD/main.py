from flask import Flask, request, jsonify, abort
import redis
import json

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

# Route pour soumettre un calcul
@app.route('/api/calcul', methods=['POST'])
def soumettre_calcul():
    data = request.get_json()
    operation = data.get("operation")
    nb1 = data.get("nb1")
    nb2 = data.get("nb2")

    if not operation or not nb1 or not nb2:
        abort(400, "Paramètres manquants")

    # Créer un message JSON avec les informations du calcul
    message = json.dumps({"operation": operation, "nb1": nb1, "nb2": nb2})

    # Placer le message dans la queue Redis
    redis_conn.lpush("calcul_queue", message)

    return jsonify({"message": "Calcul en attente de traitement"})

# Route pour récupérer le résultat d'un calcul
@app.route('/api/resultat/<int:id_resultat>', methods=['GET'])
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

# Fonction pour traiter les calculs en attente dans la queue
def traiter_calculs():
    while True:
        # Récupérer un message de la queue
        message = redis_conn.rpop("calcul_queue")

        # Si la queue est vide, sortir de la boucle
        if not message:
            break

        # Décoder le message JSON
        calcul_info = json.loads(message)

        # Effectuer le calcul
        resultat = effectuer_calcul(calcul_info["operation"], calcul_info["nb1"], calcul_info["nb2"])

        # Stocker le résultat dans Redis
        redis_conn.set("resultat_" + str(id(resultat)), str(resultat))

# Exécuter la fonction de traitement des calculs au démarrage de l'application
traiter_calculs()

if __name__ == '__main__':
    app.run(debug=True)
