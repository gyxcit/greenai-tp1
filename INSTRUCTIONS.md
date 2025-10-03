# 🌱 Green AI Data Story - Instructions Complètes

## 📱 Application créée

Votre application Streamlit **Green AI Data Story** est maintenant prête ! Elle contient :

### 🎯 Fonctionnalités principales
- **4 sections d'analyse** comme demandé
- **Visualisations interactives** avec Plotly
- **Comparaisons détaillées** entre modèles et catégories
- **Filtres dynamiques** pour explorer les données
- **Interface intuitive** avec navigation par onglets

### 📊 Structure de l'application

#### 1. **Analyse par Catégorie**
- Analyse spécifique pour chaque type de modèle (small, medium, large)
- Métriques de consommation et performance
- Graphiques en barres et scatter plots

#### 2. **Comparaison entre Catégories**
- Vue d'ensemble des 3 catégories de modèles
- Graphiques comparatifs de consommation
- Analyse des tendances par catégorie

#### 3. **Comparaison Générale des Modèles**
- Comparaison directe entre tous les modèles A et B
- Scatter plots interactifs
- Radar charts des performances

#### 4. **Analyse par Question Category**
- Focus sur les types de questions
- Impact sur la consommation énergétique
- Histogrammes et box plots

## 🚀 Comment utiliser l'application

### Option 1: Lancement direct (Python)
```bash
# Naviguer dans le dossier
cd "C:\Users\regis\OneDrive\Documents\pge5\green ai\code\tp1"

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

### Option 2: Avec Docker (Recommandé)

#### 1. Installer Docker Desktop
- Télécharger : https://www.docker.com/products/docker-desktop/
- Installer et démarrer Docker Desktop
- Vérifier : `docker --version`

#### 2. Démarrer l'application
```bash
# Naviguer dans le dossier
cd "C:\Users\regis\OneDrive\Documents\pge5\green ai\code\tp1"

# Démarrer avec Docker Compose
docker-compose up --build

# OU utiliser le script automatique
.\build-docker.bat
```

#### 3. Accéder à l'application
Ouvrir votre navigateur à : **http://localhost:8501**

## 📁 Fichiers créés

### Application principale
- `app.py` - Application Streamlit complète
- `requirements.txt` - Dépendances Python

### Configuration Docker
- `Dockerfile` - Image Docker avec Python 3.11
- `docker-compose.yml` - Orchestration des services
- `.dockerignore` - Optimisation du build
- `build-docker.bat` - Script Windows automatique
- `build-docker.sh` - Script Linux/Mac automatique

### Documentation
- `README-Docker.md` - Guide Docker détaillé
- `INSTRUCTIONS.md` - Ce fichier d'instructions

## 🎮 Navigation dans l'application

1. **Démarrer l'application** (méthode Python ou Docker)
2. **Aller sur http://localhost:8501**
3. **Explorer les 4 onglets** :
   - 📊 Analyse par Catégorie
   - 🔄 Comparaison entre Catégories  
   - 🎯 Comparaison Générale des Modèles
   - 📝 Analyse par Question Category
4. **Utiliser les filtres** pour personnaliser les vues
5. **Interagir avec les graphiques** (zoom, hover, sélection)

## 🔧 Personnalisation

### Modifier les données
- Remplacer le fichier `green Ai - Unpivoted (1).csv`
- L'application se recharge automatiquement

### Ajuster les visualisations
- Modifier `app.py` selon vos besoins
- Redémarrer l'application pour voir les changements

### Thème et style
- Streamlit utilise un thème sombre par défaut
- Personnalisable via les paramètres Streamlit

## 🌟 Avantages de cette solution

### ✅ Conformité à votre demande
- **4 sections** comme spécifié
- **Analyses par catégorie** de modèles
- **Comparaisons multiples** (catégories, modèles, questions)
- **Visualisations riches** et interactives

### ✅ Technologies modernes
- **Streamlit** : Interface web moderne et reactive
- **Plotly** : Graphiques interactifs professionnels
- **Docker** : Déploiement portable et fiable
- **Python** : Écosystème data science complet

### ✅ Facilité d'utilisation
- **Interface intuitive** avec navigation par onglets
- **Filtres dynamiques** pour explorer les données
- **Responsive design** qui s'adapte à tous les écrans
- **Documentation complète** pour installation et usage

## 🎯 Prochaines étapes

1. **Installer Docker Desktop** (si pas encore fait)
2. **Tester l'application** avec `docker-compose up --build`
3. **Explorer les 4 sections** d'analyse
4. **Personnaliser** selon vos besoins spécifiques
5. **Déployer** en production si nécessaire

## 🆘 Support

En cas de problème :
1. Vérifier que Docker Desktop est démarré
2. S'assurer que le port 8501 est libre
3. Consulter les logs avec `docker-compose logs`
4. Vérifier que tous les fichiers sont présents

**Votre application Green AI Data Story est prête à être utilisée ! 🎉**