# Projet Web Hiver 2020-2021
Ce projet consiste à créer une application web, qui s'exécute dans un navigateur. 
Cette application est un gestionnaire de données, plus précisément un gestionnaire de commandes en ligne.

Tout d’abord vu que l’application possède une BD héberger localement, 
il faut importer les fichiers JSON suivant ci dessous

le nom de la bd : `GestionCommandesBD`

| Nom fichier json        | Type de données          | Description          |
| ------------- |:-------------:|-------------|
| categorie.json       | Les catégories de produit. | Les catégorie pour les produits. |
| produit.json      | Les produits.      | Permet d'avoir des produits en stock et en rupture. |
| utilisateur.json | Les utilisateurs.      | Permet d'avoir un usager admin et non admin. |

> *les fichiers sont dans le repos git, donc dans le projet.*

Afin d'importer, ces fichiers :
1. Ouvrir mongoDB Compass
2. Se connecter: `mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false`
3. En bas à gauche, il y a un bouton **+** pour créer une BD. Une fois ce bouton appuyé, il va avoir une fenêtre qui va
   s'ouvrir. Il faut entrer dans le champ 'Database Name' le nom de la bd :` GestionCommandesBD`, il est obligatoire de
   mettre un nom de collection, donc dans le champ 'Collection Name' vous pouvez mettre le nom `produit`.
4. Une fois que la bd est crée, il faut importer les fichiers json (ceux du tableau). Il faut créer une collection pour chaque fichier 
   (dois avoir le même nom que le fichier json). Par la suite, il faut sélectionner la collection ou ont veut importer un fichier, appuyer
   sur le bouton vert **import data**, une fenêtre va s'ouvrir. Dans le **Select File** il faut mettre le chemin d'accès au
   fichier JSON, puis sélectionner **JSON** puis appuyer sur **import**. Une fois que c'est fini vous pouvez appuyer sur Done
   pour fermer la fenêtre.
5. Répéter les étapes pour tous les fichiers JSON.


Maintenant, la bd est créée et le projet est installé sur votre poste. 

Il reste a installé le requirement.
Vous pouvez utiliser un environment virtuel ou les installer directement sur votre poste (déconseiller).
1. pour crée un venv : `python -m venv lePath`
2. activée le venv : `/venv/Scripts/activate`
3. puis pour installer les requirements : `pip install -r requirements.txt`
4. Ces commande doivent être faites dans le terminal en bas de la fenêtre de pycharm.

Maintenant, pour lancer le serveur, donc le site web il faut faire cette commande dans la console :
`python manage.py runserver --insecure`
**IMPORTANT** il faut avoir **--insecure** *sinon les pages d'erreurs ne fonctionne pas et la feuille de style*.

> Pour accéder au site web, il suffit de taper `http://127.0.0.1:8000/` dans un navigateur.

Si jamais vous avez une erreur lors d'une vérification avec votre pylint qui dit : *No objects members*, 
vous pouvez rajouter ceci dans les options de pylint et cela l'ignore.
Pylint Arguments: 
`--load-plugins pylint_django --django-settings-module projet_gestion_commandes.settings --generated-members=objects`


###### Antoine Bédard & Anthony Levesque - 2021
