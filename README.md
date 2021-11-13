# Programme ETL sur un site école :
Extraction, Transformation et Chargement de données sur le site  : https://books.toscrape.com

	# 1 : Premier programme : ETL_page_produit,
	dans un page 'livre' donné (Http du livre), extrait les données demandés et créé un fichier csv pour les télécharger

	
	# 2 : Deuxième programme : ETL_page_category,
	dans une catégorie donnée (Http de la catégorie), extrait les liens des livres contenus dans cette catégorie et met en application le premier programme
	il charge dans un fichier csv toutes les données par livre

	# 3 : Troisième et dernier programme : ETL_site_books
	sur le site, il extrait les liens de toutes les catégories, extrait les liens de chaque livre inclus dans chaque catégorie et extrait les données demandées par livre
	il crée un fichier csv par catégorie : # ! Créer en amont un dossier "books" pour intégrer l'ensemble des fichiers csv créés
	puis il crée un fichier image (png) par livre parcouru : # ! Créer en amont un dossier "images' pour intégrer l'ensemble des fichiers image créés

	# 4 : requirements : 1 seul fichier pour l'ensemble des 3 programmes (mêmes packages utilisés)


# Création de l'environnement virtuel :
Avec le terminal, dans le dossier de travail, éditer un environnement virtuel avec la commande suivante (pour une console Ubuntu) : 
python3 -m venv env

Puis activer cette environnement pour pouvoir y intégrer les packages utiles u fonctionnement des programmes écrits ci dessus :
source env/bin/activate

Une fois activé (env) : installer les packages utiles

Pour sortir de l'environnment virtuel, taper : 
deactivate
à tout moment il est possible de réactiver l'environnmenet virtuel pour y intégrer de nouveaux packages utiles

à la fin de l'écriture du programme, actviver l'environnement virtuel et taper la commande : 
pip freeze > requirements.txt
ce fichier txt reprendra la liste de l'ensemble des packages installés et utiles au lancement du programme

 