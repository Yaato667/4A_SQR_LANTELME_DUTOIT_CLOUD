from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Fonction pour enregistrer un tweet dans Redis
def enregistrer_tweet(tweet_id, tweet_text, username, hashtags):
    tweet_data = {
        'tweet_id': tweet_id,
        'tweet_text': tweet_text,
        'username': username,
        'hashtags': hashtags
    }
    redis_client.hmset(f'tweet:{tweet_id}', tweet_data)

# Fonction pour afficher tous les tweets
@app.route('/tweets', methods=['GET'])
def afficher_tweets():
    keys = redis_client.keys('tweet:*')
    tweets = [redis_client.hgetall(key) for key in keys]
    return jsonify(tweets)

# Fonction pour afficher les tweets liés à une personne
@app.route('/tweets/<username>', methods=['GET'])
def afficher_tweets_utilisateur(username):
    keys = redis_client.keys('tweet:*')
    user_tweets = [redis_client.hgetall(key) for key in keys if redis_client.hget(key, 'username') == username]
    return jsonify(user_tweets)

# Fonction pour retweeter un tweet
@app.route('/tweets/retweet', methods=['POST'])
def retweeter_tweet():
    data = request.json
    tweet_id = data['tweet_id']
    # Simuler le retweet en incrémentant le compteur de retweets
    redis_client.hincrby(f'tweet:{tweet_id}', 'retweet_count', 1)
    return jsonify({'message': f'Tweet {tweet_id} retweeté avec succès'})

# Fonction pour afficher les sujets
@app.route('/sujets', methods=['GET'])
def afficher_sujets():
    keys = redis_client.keys('h-hashtag:*')
    sujets = [key.decode('utf-8').split(':')[-1] for key in keys]
    return jsonify(sujets)

# Fonction pour afficher les tweets liés à un sujet
@app.route('/sujets/<hashtag>', methods=['GET'])
def afficher_tweets_sujet(hashtag):
    keys = redis_client.keys(f'h-hashtag:{hashtag}:*')
    sujet_tweets = [redis_client.hgetall(key) for key in keys]
    return jsonify(sujet_tweets)

if __name__ == '__main__':
    app.run(debug=True)
