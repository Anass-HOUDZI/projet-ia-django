# 🏛️ France étrangers (Projet IA Django)

Assistant administratif 100% piloté par l'IA pour centraliser et automatiser les démarches des étrangers en France.

## 👥 L'Équipe
* **Barakissa** 
* **Nassim**
* **Anass**

## 🛠️ Prérequis
* Python 3.10+
* Git

## 🚀 Installation & Démarrage (Local)

1. **Cloner le projet et se placer sur la branche develop**
   ```bash
   git clone https://github.com/Anass-HOUDZI/projet-ia-django.git
   cd projet-ia-django
   git checkout develop
   ```

2. **Créer et activer l'environnement virtuel**
   ```bash
   python -m venv venv
   # Sur Windows :
   venv\Scripts\activate
   # Sur Mac/Linux :
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   - Copier le fichier `.env.example` et le renommer en `.env`.
   - Remplir les clés API nécessaires à l'intérieur.

5. **Initialiser la base de données**
   ```bash
   python manage.py migrate
   ```

6. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```
