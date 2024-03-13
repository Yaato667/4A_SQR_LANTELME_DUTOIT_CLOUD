# 4A_SQR_LANTELME_DUTOIT_CLOUD

## Noms des auteurs
[Dutoit Arthur](https://github.com/Aasa21)

[Lantelme Tom](https://github.com/Yaato667) 

# Projet

## Technologies utilisées 

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54g">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E">
</p>


## Explication du sujet

Création d'un clone de Tweeter
Ce clone sera divisé en deux parties : 
- Une partie beckend qui sera composée d'une utilisation de redis ainsi qu'une api en python
- Une partie frontend qui sera un site internet permettant d'utiliser l'api de manière bien plus agréable qu'avec un terminal
  
### Réalisation d'une première version de l'API REST
  
Commande CURL:

Ajouter un tweet :
````
curl -X POST -H "Content-Type: application/json" -d "{\"tweet_id\": \"1\", \"tweet_text\": \"Contenu du tweet\", \"username\": \"utilisateur\", \"hashtags\": [\"sujet1\", \"sujet2\"]}" http://localhost:5000/tweets
````
Afficher tous les tweets :
````
curl http://localhost:5000/tweets
````
Afficher les tweets d'un utilisateur :
````
curl http://localhost:5000/tweets/utilisateur
````
Retweeter un tweet :
````
curl -X POST -H "Content-Type: application/json" -d "{\"tweet_id\": \"1\"}" http://localhost:5000/tweets/retweet
````
Afficher tous les sujets :
````
curl http://localhost:5000/sujets
````
Afficher les tweets pour un sujet spécifique :
````
curl http://localhost:5000/sujets/sujet
````
Supprimer un tweet (remplacez 1 par l'identifiant du tweet à supprimer) :
````
curl -X DELETE http://localhost:5000/tweets/1
````

  
### Création de github actions

[![badge](https://img.shields.io/badge/PROJET_TERMINÉ_🚀-059142?style=for-the-badge&logoColor=white)](https://dev.to/envoy_/150-badges-for-github-pnk)

![badge](https://github.com/Yaato667/4A_SQR_LANTELME_DUTOIT_CLOUD/actions/workflows/Hello_PR.yml/badge.svg)
![badge](https://github.com/Yaato667/4A_SQR_LANTELME_DUTOIT_CLOUD/actions/workflows/Moon_Curl.yml/badge.svg)
![badge](https://github.com/Yaato667/4A_SQR_LANTELME_DUTOIT_CLOUD/actions/workflows/push.yml/badge.svg)
