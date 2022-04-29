# Cliday-backend-django

Projet déployé à l'url : https://murmuring-fjord-44933.herokuapp.com 


On peut faire des requêtes directement à cette adresse pour tester l'api 

Procédure d'installation :

S'assurer d'avoir pip et github cli d'installé.

```
gh repo clone MysteryHS/Cliday-backend-django
cd .\Cliday-backend-django\
pip install -r requirements.txt
```
Copier une clé à l'adresse https://djecrety.ir/ 


Rajouter dans le fichier project/settings.py la ligne SECRET_KEY = 'votre_cle'
```
python manage.py migrate
python manage.py runserver
```

Le serveur tourne alors à l'adresse http://127.0.0.1:8000/
Vous pouvez faire des requetes http à cette adresse ou créer un superuser avec la commande ```python manage.py createsuperuser```
et aller à http://127.0.0.1:8000/admin afin d'accéder à l'interface admin.

contact : ducastel.mateo@laposte.net
