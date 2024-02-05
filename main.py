from flask import Flask, request, jsonify, abort
from datetime import datetime
import csv
import sys

# Création de l'appli Flask
app = Flask(__name__)

# Liste pour stocker les évents
events = []

# Creation de event avec POST
@app.route('/events', methods=['POST'])
def create_event():
    # Récupération des données JSON de la requête
    data = request.get_json()

    # Création d'un dico 
    event = {
        'T1': data.get('T1'),
        't': data.get('t'),
        'p': data.get('p'),
        'n': data.get('n')
    }

    # Ajout à la liste
    events.append(event)

    # Succès
    return 'Événement ajouté, bien joué', 201

# Afficher une liste de tous les événements dans l’ordre chronologique
@app.route('/events', methods=['GET'])
def get_all_events():
    # Trie la liste des évènements en utilisant la fonction sort_by_timestamp comme clé de tri
    sorted_events = sorted(events, key=sort_by_timestamp)
    # Retourne un dictionnaire JSON contenant la liste triée des évènements
    return jsonify({'events': sorted_events})

# Fonction auxiliaire pour définir la clé de tri par timestamp
def sort_by_timestamp(event):
    # Extrait la valeur associée à la clé 'T1' de l'évènement
    timestamp_str = event.get('T1')

    # Vérifie si la valeur est présente et non vide
    if timestamp_str:
        # Convertit la chaîne d'heure en objet de temps
        return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
    else:
        # Si la valeur est manquante ou vide, retourne une date minimale
        return datetime.min

# E3 - Afficher une liste de tous les évènements dans l’ordre chronologique liées à une personne

# Fonction de tri par date pour les événements
def sort_events_by_date(event):
    return datetime.strptime(event.get('T1', ''), '%Y-%m-%dT%H:%M:%S')

# Route API pour récupérer les événements liés à une personne dans le bon ordre
@app.route("/events/person/<person_name>", methods=['GET'])
def get_events_by_person(person_name):
    # Filtrer pour chaque personne
    person_events = [event for event in events if person_name in event.get('p', [])]

    # Trier par date quand même
    sorted_person_events = sorted(person_events, key=sort_events_by_date)

    return jsonify({'events': sorted_person_events})

# Endpoint pour ajouter un participant à un évènement spécifié par son ID
@app.route('/events/<event_name>/add-participant', methods=['POST'])
def add_participant_by_name(event_name):
    # Recherche de l'évènement correspondant au nom dans la liste des évènements
    event = next((event for event in events if event.get('n') == event_name), None)
    
    # Vérifie si l'évènement a été trouvé
    if event:
        # Récupération des données JSON de la requête
        data = request.get_json()
        
        # Ajout du participant à la liste des participants de l'évènement
        # Si la clé 'p' n'existe pas, elle est créée avec une liste vide comme valeur par défaut
        event.setdefault('p', []).append(data.get('participant'))
        
        # Retourne un message indiquant que le participant a été ajouté avec succès et le code HTTP 200 (OK)
        return 'Participant ajouté avec succès à l\'événement "{}" !'.format(event_name), 200
    else:
        # Si l'évènement n'est pas trouvé, retourne une erreur 404 avec un message correspondant
        abort(404, 'Évènement "{}" non trouvé')

# Route pour obtenir les détails du prochain cours en fonction de l'heure actuelle
@app.route('/events/next-course', methods=['GET'])
def get_next_course():
    if events:
        # Récupérer l'heure actuelle
        current_time = datetime.now()
        print("Heure actuelle:", current_time)
        
        # Filtrer les événements à venir (après ou à l'heure actuelle)
        upcoming_events = [event for event in events if sort_by_timestamp(event) >= current_time]
        print("Événements à venir:", upcoming_events)
        
        if upcoming_events:
            # Trouver l'événement avec le timestamp minimum 
            next_course = min(upcoming_events, key=sort_by_timestamp)
            print("Prochain cours:", next_course)
            return jsonify({'next_course': next_course})
        else:
            # Retourner une erreur 404 s'il n'y a aucun événement à venir
            abort(404, 'Aucun évènement à venir')
    else:
        # Retourner une erreur 404 s'il n'y a aucun événement disponible
        abort(404, 'Aucun évènement trouvé')

# Route pour télécharger des événements depuis un fichier CSV
@app.route('/uploadevents', methods=['POST'])
def upload_events():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Lecture du fichier CSV
    csv_data = file.read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_data)

    for row in csv_reader:
        timestamp = row.get('timestamp')
        event_name = row.get('event_name')
        attendees = row.get('attendees')
        time = row.get('atime')
        
        # Ajout de vérification pour éviter la conversion avec une valeur None
        if timestamp:
            events.append({'T1': timestamp, 'n': event_name, 'p': attendees, 't': time})

    return jsonify({'message': 'File uploaded successfully'}), 201

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_syntax":
            print("Build [ OK ]")
            exit(0)
        else:
            print("L'argument fourni n'est pas pris en charge ! Argument pris en charge : check_syntax")
            exit(1)
    app.run(debug=True)


