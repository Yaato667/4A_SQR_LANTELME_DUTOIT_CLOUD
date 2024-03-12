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


// Fonction pour supprimer un tweet
function supprimerTweet(tweetId) {
    fetch(`http://localhost:5000/tweets/${tweetId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Affiche un message indiquant que le tweet a été supprimé
        afficherTousLesTweets(); // Rafraîchit la liste des tweets après la suppression
    })
    .catch(error => console.error('Erreur lors de la suppression du tweet:', error));
}


// Fonction pour retweeter un tweet
function retweeterTweet(tweetId) {
    fetch('http://localhost:5000/tweets/retweet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tweet_id: tweetId })
    })
    .then(response => response.json())
    .then(data => afficherResultat(data))
    .catch(error => console.error('Erreur lors du retweet:', error));
}

// Fonction pour ajouter un nouveau tweet
function ajouterNouveauTweet(event) {
    event.preventDefault();

    // Récupérer les valeurs des champs du formulaire
    const tweetText = document.getElementById('tweet-text').value;
    const username = document.getElementById('tweet-username').value;
    const hashtags = document.getElementById('tweet-hashtags').value.split(' '); // Diviser les hashtags en une liste

    // Générer un ID unique pour le tweet (peut être remplacé par un système plus robuste)
    const tweetId = Math.floor(Math.random() * 1000000);

    // Créer l'objet JSON contenant les données du tweet
    const tweetData = {
        tweet_id: tweetId,
        tweet_text: tweetText,
        username: username,
        hashtags: hashtags
    };

    // Effectuer une requête POST pour ajouter le tweet
    fetch('http://localhost:5000/tweets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tweetData)
    })
    .then(response => response.json())
    .then(data => {
        // Afficher un message indiquant que le tweet a été ajouté avec succès
        alert(data.message);

        // Effacer les champs du formulaire après l'ajout du tweet
        document.getElementById('tweet-text').value = '';
        document.getElementById('tweet-username').value = '';
        document.getElementById('tweet-hashtags').value = '';
    })
    .catch(error => console.error('Erreur lors de l\'ajout du tweet:', error));
}
