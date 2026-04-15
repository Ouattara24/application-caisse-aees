# 🚀 Déploiement AEES - Guide Complet

## Option 1 : Ngrok (Rapide - Test)

### Installation de Ngrok :
1. Allez sur https://ngrok.com/download
2. Téléchargez la version Windows
3. Extrayez le fichier `ngrok.exe`
4. Placez-le dans un dossier accessible (ex: `C:\ngrok\ngrok.exe`)

### Utilisation :
```bash
# Dans un terminal séparé, avec le serveur Django déjà lancé :
ngrok http 8000
```

Ngrok vous donnera une URL comme : `https://abc123.ngrok.io`

**Partagez cette URL** aux utilisateurs pour qu'ils installent l'app !

---

## Option 2 : Heroku (Recommandé - Production)

### Installation :
1. Créez un compte sur https://heroku.com
2. Installez Heroku CLI : https://devcenter.heroku.com/articles/heroku-cli

### Déploiement :
```bash
# Créer l'app Heroku
heroku create votre-app-aees

# Déployer
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a votre-app-aees
git push heroku main

# Ouvrir l'app
heroku open
```

**Avantages** : URL permanente, SSL gratuit, évolutif

---

## Option 3 : Railway (Simple)

1. Allez sur https://railway.app
2. Connectez votre GitHub
3. Déployez directement depuis le repo
4. Obtenez une URL comme `https://aees-production.up.railway.app`

---

## Option 4 : VPS (Avancé)

Utilisez DigitalOcean, Linode, ou OVH pour un serveur dédié.

### Configuration requise :
- Ubuntu/Debian
- Python 3.12+
- PostgreSQL (recommandé pour production)
- Nginx + Gunicorn

---

## 📱 Instructions pour les Utilisateurs

Une fois l'URL publique obtenue (ex: `https://votredomaine.com`) :

1. **Sur téléphone** : Ouvrir Chrome/Safari
2. **Aller sur l'URL** fournie
3. **Installer** : Menu "Ajouter à l'écran d'accueil"
4. **L'app AEES** sera installée avec le logo !

---

## ⚙️ Configuration Production

Avant déploiement, modifiez `settings.py` :

```python
DEBUG = False
ALLOWED_HOSTS = ['votredomaine.com', 'www.votredomaine.com']

# Pour Railway/Heroku :
import os
ALLOWED_HOSTS = [os.environ.get('RAILWAY_STATIC_URL', 'localhost'), '127.0.0.1']

# Base de données production :
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}
```

---

## 🔗 Liens Utiles

- **Ngrok** : https://ngrok.com
- **Heroku** : https://heroku.com
- **Railway** : https://railway.app
- **Django Deployment** : https://docs.djangoproject.com/en/4.2/howto/deployment/

**Choisissez l'option qui vous convient le mieux !** 🎯