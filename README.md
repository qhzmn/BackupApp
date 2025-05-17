# 🗂️ BackupApp – Outil de Sauvegarde Incrémentielle avec Interface Graphique

Une application Python avec une interface graphique basée sur Tkinter. Elle permet de réaliser des sauvegardes incrémentielles de dossiers sélectionnés vers un répertoire de destination, tout en enregistrant un historique dans un fichier Markdown.

---

## 🚀 Fonctionnalités

- ✅ Sélection de plusieurs dossiers source
- ✅ Choix du dossier de destination
- ✅ Sauvegarde incrémentielle (copie uniquement les fichiers nouveaux ou modifiés)
- ✅ Enregistrement de l’historique des sauvegardes dans un fichier `.md`
- ✅ Barre de progression de la sauvegarde
- ✅ Sauvegarde et rechargement automatiques des chemins utilisés
- ✅ Interface graphique simple et intuitive
- ✅ Journalisation des actions dans `app.log`

---

## 🖼️ Aperçu de l’interface

L’interface contient :
- Une liste de dossiers source sélectionnés (avec options Ajouter / Supprimer)
- Un champ pour sélectionner le dossier de destination
- Un champ pour sélectionner un fichier historique `.md`
- Une barre de progression
- Des champs pour nommer les dossiers source et destination
- Un bouton Effacer tout pour réinitialiser les champs

---

## 🛠️ Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/ton-nom-utilisateur/backupapp.git
```

### 2. Prérequis
- Python 3.7 ou supérieur
- Aucune bibliothèque externe n’est requise (seulement la bibliothèque standard de Python)

### 3. Lancer l'application
```bash
python backup_app.py
```

### 4. Transformation en Exécutable (.exe)
Pour transformer le script Python en un exécutable autonome (`.exe`), vous pouvez utiliser PyInstaller. Voici les étapes à suivre :
- Assurez-vous d'abord que PyInstaller est installé. Vous pouvez l'installer via pip :
```bash
pip install pyinstaller
```
- Navigue dans le dossier contenant ton script Python :
```bash
cd chemin/vers/ton/script
```
- Génère le fichier exécutable :
```bash
pyinstaller --onefile --windowed ton_script.py
```

---

## 🧩 Structure des fichiers
```bash
├── backup_app.py       # Script principal de l'application
├── paths.json          # Fichier auto-généré des chemins enregistrés
├── app.log             # Journal des actions (auto-généré)
└── README.md           # Documentation
```

---

## 📄 Format du fichier Markdown
À chaque sauvegarde, une ligne est ajoutée au fichier .md sélectionné sous le format :

```bash
| YYYY-MM-DD | Nom du dossier source      | Incremental  | Nom du dossier destination | Succes         |
```
Les noms sont tronqués ou complétés automatiquement pour conserver un tableau aligné.

---

## ⚙️ Fonctionnement
- Utilise shutil.copy2 pour copier les fichiers tout en conservant les métadonnées.
- La sauvegarde est dite incrémentielle : seuls les fichiers nouveaux ou modifiés sont copiés.
- Les chemins sélectionnés sont enregistrés automatiquement dans un fichier paths.json.
- Toutes les actions sont enregistrées dans un fichier app.log.

---

## 🧼 Fonction Réinitialiser
Le bouton "Effacer tout" :
- Vide tous les champs et listes
- Réinitialise paths.json
- Journalise l’action dans le fichier app.log

---

## 📌 Limitations Connues
- Aucune fonctionnalité de restauration des sauvegardes
- Pas de gestion des conflits ou fichiers verrouillés
- Les fichiers cachés ou liens symboliques ne sont pas explicitement gérés
