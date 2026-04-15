# 🚀 Guide Rapide : Obtenir un Lien Public pour Votre App AEES

## Option 1 : Ngrok (Test/Partage Immédiat - 5 minutes)

### 📥 Installation de Ngrok :
1. Téléchargez : https://ngrok.com/download
2. Choisissez **Windows** > **Download for Windows**
3. Extrayez le fichier `ngrok.exe` dans `C:\ngrok\`

### 🔗 Créer un lien public :
```bash
# Ouvrez un NOUVEAU terminal PowerShell
cd C:\ngrok
.\ngrok.exe http 8000
```

**Ngrok vous donne une URL comme : `https://abc123.ngrok.io`**

**🎉 Partagez cette URL HTTPS aux utilisateurs !**

Ils pourront :
- Ouvrir l'URL sur leur téléphone
- Cliquer "Ajouter à l'écran d'accueil"
- Installer l'app AEES !

---

## Option 2 : Railway (Production - Recommandé)

### Suivez ces étapes :

1. **GitHub** : Créez un compte sur https://github.com
2. **Upload** : Poussez votre code sur GitHub
3. **Railway** : https://railway.app > "Deploy from GitHub"
4. **URL permanente** : `https://votrenom.up.railway.app`

### Avantages Railway :
- ✅ URL fixe et HTTPS
- ✅ Gratuit pour commencer
- ✅ Base de données incluse
- ✅ Déploiement automatique

---

## 📱 Instructions pour les Utilisateurs

Une fois l'URL obtenue :

1. **Sur téléphone** : Ouvrir Chrome/Safari
2. **Coller l'URL** (celle de ngrok ou Railway)
3. **Menu** : "Ajouter à l'écran d'accueil"
4. **Installer** : L'app AEES apparaît sur l'écran d'accueil !

---

## ⚡ Test Rapide :

**Votre serveur tourne sur http://127.0.0.1:8000/**

Pour le partage : **Installez ngrok** et lancez `ngrok http 8000` !

**Vous aurez votre lien public en 2 minutes !** 🚀