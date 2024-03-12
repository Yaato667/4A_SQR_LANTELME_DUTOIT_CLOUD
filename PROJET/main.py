from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)  # Active CORS pour toute l'application
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Fonction pour enregistrer un tweet dans Redis
def enregistrer_tweet(tweet_id, tweet_text, username, hashtags):
    # Convertir la liste de hashtags en une chaîne de caractères
    hashtags_str = ' '.join(hashtags)
    
    tweet_data = {
        'tweet_id': tweet_id,
        'tweet_text': tweet_text,
        'username': username,
        'hashtags': hashtags_str,  # Utiliser la chaîne de caractères des hashtags
        'retweet_count': 0  # Initialiser le compteur de retweets à 0
    }
    redis_client.hmset(f'tweet:{tweet_id}', tweet_data)
    
    # Enregistrer les hashtags associés au tweet
    for hashtag in hashtags:
        redis_client.sadd(f'h-hashtag:{hashtag}', f'tweet:{tweet_id}')


# Route pour ajouter un tweet avec la méthode POST
@app.route('/tweets', methods=['POST'])
def ajouter_tweet():
    data = request.json
    tweet_id = data['tweet_id']
    tweet_text = data['tweet_text']
    username = data['username']
    hashtags = data['hashtags']
    
    # Appel à la fonction pour enregistrer le tweet
    enregistrer_tweet(tweet_id, tweet_text, username, hashtags)
    
    return jsonify({'message': f'Tweet {tweet_id} ajouté avec succès'})
