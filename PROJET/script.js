// Fonction pour afficher tous les tweets
function afficherTousLesTweets() {
    fetch('http://localhost:5000/tweets')
        .then(response => response.json())
        .then(data => afficherResultat(data))
        .catch(error => console.error('Erreur lors de la récupération des tweets:', error));
}

// Fonction pour afficher les tweets d'un utilisateur
function afficherTweetsUtilisateur(event) {
    event.preventDefault();
    const username = document.getElementById('username').value; // Utilisez document.getElementById pour récupérer la valeur
    fetch(`http://localhost:5000/tweets/${username}`)
        .then(response => response.json())
        .then(data => afficherResultat(data))
        .catch(error => console.error('Erreur lors de la récupération des tweets de l\'utilisateur:', error));
}

// Fonction pour afficher les sujets
function afficherSujets() {
    fetch('http://localhost:5000/sujets')
        .then(response => response.json())
        .then(data => {
            const resultContainer = document.getElementById('result-container');
            resultContainer.innerHTML = '<h2>Sujets :</h2>';
            if (Array.isArray(data) && data.length > 0) {
                const sujetsList = document.createElement('ul');
                data.forEach(sujet => {
                    const sujetItem = document.createElement('li');
                    sujetItem.textContent = sujet;
                    sujetsList.appendChild(sujetItem);
                });
                resultContainer.appendChild(sujetsList);
            } else {
                resultContainer.innerHTML = '<p>Aucun sujet trouvé.</p>';
            }
        })
        .catch(error => console.error('Erreur lors de la récupération des sujets:', error));
}

// Fonction pour afficher les tweets liés à un sujet
function afficherTweetsSujet(event) {
    event.preventDefault();
    const hashtag = event.target.hashtag.value;
    fetch(`http://localhost:5000/sujets/${hashtag}`)
        .then(response => response.json())
        .then(data => afficherResultat(data))
        .catch(error => console.error('Erreur lors de la récupération des tweets du sujet:', error));
}

// Fonction pour afficher les résultats
function afficherResultat(data) {
    const resultContainer = document.getElementById('result-container');
    resultContainer.innerHTML = '<h2>Résultat :</h2>';
    if (Array.isArray(data) && data.length > 0) {
        data.forEach(item => {
            const tweetDiv = document.createElement('div');
            tweetDiv.classList.add('tweet');
            tweetDiv.innerHTML = `
                <p class="username">Utilisateur: ${item.username}</p>
                <p>Contenu: ${item.tweet_text}</p>
                <p class="hashtags">Hashtags: ${item.hashtags}</p>
                <p>Nombre de retweets: ${item.retweets}</p>
                <button class="retweet-btn" data-tweet-id="${item.tweet_id}">Retweeter</button>
                <button class="delete-btn" data-tweet-id="${item.tweet_id}">Supprimer</button>
            `;
            resultContainer.appendChild(tweetDiv);
            
            // Ajouter un événement de clic au bouton Retweeter
            tweetDiv.querySelector('.retweet-btn').addEventListener('click', () => {
                retweeterTweet(item.tweet_id);
            });

            // Ajouter un événement de clic au bouton Supprimer
            tweetDiv.querySelector('.delete-btn').addEventListener('click', () => {
                supprimerTweet(item.tweet_id);
            });
        });
    } else {
        resultContainer.innerHTML = '<p>Aucun résultat trouvé.</p>';
    }
}

