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

@app.route('/tweets', methods=['GET'])
def afficher_tweets():
    keys = redis_client.keys('tweet:*')
    tweets = []
    for key in keys:
        tweet_data = redis_client.hgetall(key)
        tweet = {key.decode('utf-8'): value.decode('utf-8') for key, value in tweet_data.items()}
        tweet['retweets'] = int(redis_client.hget(key, 'retweet_count') or 0)
        tweets.append(tweet)
    return jsonify(tweets)


# Fonction pour afficher les tweets liés à une personne
@app.route('/tweets/<username>', methods=['GET'])
def afficher_tweets_utilisateur(username):
    # Utilisation d'une liste en compréhension pour récupérer les tweets de l'utilisateur
    user_tweets = []
    for key in redis_client.keys('tweet:*'):  # Parcourir toutes les clés correspondant au motif 'tweet:*'
        if (username_bytes := redis_client.hget(key, 'username')) is not None:  # Vérifier si le champ 'username' existe
            decoded_username = username_bytes.decode('utf-8')
            if decoded_username == username:  # Décoder le champ 'username' et le comparer à l'utilisateur demandé
                tweet = {k.decode('utf-8'): v.decode('utf-8') for k, v in redis_client.hgetall(key).items()}  # Décodez les clés et les valeurs en bytes en chaînes de caractères
                # Récupérer le nombre de retweets pour ce tweet
                tweet['retweets'] = int(redis_client.hget(key, 'retweet_count') or 0)
                user_tweets.append(tweet)
    return jsonify(user_tweets)


# Fonction pour retweeter un tweet
@app.route('/tweets/retweet', methods=['POST'])
def retweeter_tweet():
    data = request.json
    tweet_id = data['tweet_id']
    # Incrémenter le compteur de retweets
    redis_client.hincrby(f'tweet:{tweet_id}', 'retweet_count', 1)
    return jsonify({'message': f'Tweet {tweet_id} retweeté avec succès'})

# Fonction pour afficher les sujets
@app.route('/sujets', methods=['GET'])
def afficher_sujets():
    keys = redis_client.keys('h-hashtag:*')
    sujets = []
    for key in keys:
        sujet = key.decode('utf-8').split(':')[-1]
        sujets.append(sujet)
    return jsonify(sujets)
