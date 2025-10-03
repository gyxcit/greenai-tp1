# Green AI Data Story - Docker

Cette application Streamlit peut être facilement déployée avec Docker.

## � Prérequis

### Installation de Docker sur Windows

1. **Télécharger Docker Desktop**
   - Allez sur https://www.docker.com/products/docker-desktop/
   - Téléchargez Docker Desktop pour Windows
   - Exécutez l'installateur et suivez les instructions

2. **Vérifier l'installation**
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Démarrer Docker Desktop**
   - Lancez Docker Desktop depuis le menu Démarrer
   - Attendez que Docker soit complètement démarré (icône verte dans la barre système)

## 🐳 Déploiement avec Docker

### Option 1: Docker Compose (Recommandé)

```bash
# Naviguer dans le dossier du projet
cd "C:\Users\regis\OneDrive\Documents\pge5\green ai\code\tp1"

# Construire et démarrer l'application
docker-compose up --build

# Pour démarrer en arrière-plan
docker-compose up -d --build
```

### Option 2: Docker standard

```bash
# Construire l'image
docker build -t green-ai-app .

# Démarrer le conteneur
docker run -p 8501:8501 green-ai-app

# Pour démarrer en arrière-plan
docker run -d -p 8501:8501 --name green-ai-container green-ai-app
```

### Option 3: Script automatique (Windows)

```bash
# Double-cliquer sur le fichier ou exécuter :
.\build-docker.bat
```

## 🌐 Accès à l'application

Une fois démarrée, l'application sera accessible à :
- **URL locale**: http://localhost:8501
- **URL réseau**: http://[IP-de-votre-machine]:8501

## 🛠️ Commandes utiles

### Docker Compose
```bash
# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down

# Reconstruire l'image
docker-compose build --no-cache

# Redémarrer
docker-compose restart

# Voir l'état des services
docker-compose ps
```

### Docker standard
```bash
# Voir les logs
docker logs green-ai-container -f

# Arrêter le conteneur
docker stop green-ai-container

# Supprimer le conteneur
docker rm green-ai-container

# Voir les conteneurs en cours
docker ps

# Voir toutes les images
docker images
```

## 📁 Fichiers Docker créés

- `Dockerfile` - Configuration de l'image Docker
- `docker-compose.yml` - Configuration pour Docker Compose  
- `.dockerignore` - Fichiers à ignorer lors du build
- `build-docker.bat` - Script automatique pour Windows
- `build-docker.sh` - Script automatique pour Linux/Mac
- `README-Docker.md` - Cette documentation

## 🔧 Configuration de l'application

L'application Docker est configurée pour :
- **Port** : 8501 (standard Streamlit)
- **Mode** : Headless (sans interface graphique locale)
- **Réseau** : Accessible depuis toutes les adresses IP
- **Sécurité** : Utilisateur non-root dans le conteneur
- **Redémarrage** : Automatique en cas d'erreur

## 🚀 Avantages de Docker

1. **Portabilité** : Fonctionne de façon identique sur tous les systèmes
2. **Isolation** : Environnement séparé et contrôlé
3. **Déploiement facile** : Une seule commande pour démarrer
4. **Pas de conflits** : Indépendant de votre environnement Python local
5. **Scalabilité** : Facile à déployer sur des serveurs

## 🔍 Dépannage

### Docker Desktop ne démarre pas
- Vérifiez que la virtualisation est activée dans le BIOS
- Redémarrez votre ordinateur
- Vérifiez que WSL2 est installé sur Windows

### Port 8501 déjà utilisé
```bash
# Trouver le processus qui utilise le port
netstat -ano | findstr :8501

# Utiliser un autre port
docker run -p 8502:8501 green-ai-app
```

### Erreur de build
```bash
# Nettoyer le cache Docker
docker system prune -a

# Reconstruire sans cache
docker build --no-cache -t green-ai-app .
```

## 🌍 Déploiement en production

Pour un déploiement en production, considérez :

1. **Reverse Proxy** (nginx)
2. **HTTPS/SSL** avec certificats
3. **Variables d'environnement** pour la configuration
4. **Volumes persistants** pour les données
5. **Monitoring** et logs centralisés
6. **Mise à l'échelle** avec Docker Swarm ou Kubernetes

## 📊 Monitoring et Health Check

Le conteneur inclut :
- **Health Check** : Vérifie la disponibilité toutes les 30 secondes
- **Restart Policy** : Redémarrage automatique en cas d'erreur
- **Logs** : Accessibles via `docker logs`

## 🤝 Support

Si vous rencontrez des problèmes :
1. Vérifiez que Docker Desktop est démarré
2. Consultez les logs avec `docker-compose logs`
3. Vérifiez que le port 8501 est libre
4. Assurez-vous que tous les fichiers sont présents dans le dossier