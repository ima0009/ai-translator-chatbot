# 🌐 MERCREDI - AI-Powered Translation Assistant


> **MERCREDI** est un assistant de traduction intelligent multilingue basé sur l'IA, capable de traduire du texte, des documents, de l'audio et des images en temps réel.

---

## ✨ Fonctionnalités Principales

### 📝 Traduction Texte
- Support de **10 langues** (Français, Anglais, Arabe, Allemand, Espagnol, Italien, Japonais, Chinois, Russe, Turc)
- Détection automatique de la langue source
- Lecture audio de la traduction en temps réel

### 📄 Traduction Document
- Formats supportés : `.txt`, `.docx`, `.pdf`, `.pptx`
- Conservation du formatage original
- Traduction complète en un clic

### 🎙️ Transcription & Traduction Audio
- Support des formats : `.mp3`, `.wav`, `.ogg`, `.flac`, `.m4a`
- Transcription avec Whisper Large v3 Turbo
- Traduction et lecture audio automatique

### 🖼️ OCR & Traduction d'Image
- Extraction de texte depuis images (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`)
- Traduction directe du texte extrait
- Lecture audio du résultat

### 💬 Chatbot IA Multidomaines
- Modèle : Llama 3.3 70B (via Groq)
- Support des images et documents en conversation
- Réponses intelligentes et contextuelles

### 📋 Historique & Export
- Sauvegarde automatique de toutes les traductions
- Export en `.txt`
- Statistiques d'utilisation

### 💡 Feedback & Amélioration
- Système de notation (😍 😊 😐 😕 😞)
- Collecte structurée des retours utilisateurs
- Tableau de bord avec statistiques

---

## 🚀 Démarrage Rapide

### Installation Locale

```bash
# 1. Cloner le repository
git clone https://github.com/username/mercredi-translator.git
cd mercredi-translator

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer les secrets
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
GROQ_API_KEY = "gsk_votre_clé_groq"
OCR_API_KEY = "helloworld"  # ou votre clé OCR.space
SUPABASE_URL = "votre_url"  # optionnel
SUPABASE_KEY = "votre_clé"  # optionnel
EOF

# 5. Lancer l'app
streamlit run app.py
```

L'app sera accessible à : `http://localhost:8501`

### Déploiement sur Streamlit Cloud

```bash
# 1. Créer un repository GitHub
# 2. Push votre code
git push origin main

# 3. Aller sur https://share.streamlit.io
# 4. Déployer depuis GitHub
# 5. Ajouter les secrets dans les paramètres
```

Voir [DEPLOYMENT_GUIDE_FR.md](./DEPLOYMENT_GUIDE_FR.md) pour les instructions détaillées.

---

## 📋 Prérequis

### Comptes Requis
- **[Groq Console](https://console.groq.com)** - Clé API gratuite pour Llama 3.3 (100k tokens/jour)
- **[OCR.space](https://ocr.space/ocrapi)** - API OCR gratuite (optionnel)
- **[Supabase](https://supabase.com)** - Base de données pour feedback (optionnel)

### Configuration Système
- Python 3.8+
- 512 MB RAM minimum
- Connexion Internet active

---

## 🛠️ Technologies Utilisées

| Technologie | Usage |
|---|---|
| **Streamlit** | Interface web interactive |
| **Groq API** | Modèles LLM (Llama 3.3, Whisper) |
| **Python-docx** | Traitement de documents Word |
| **PyMuPDF** | Traitement de fichiers PDF |
| **Pillow** | Traitement d'images |
| **Pytesseract** | OCR local |
| **gTTS** | Synthèse vocale (lecture audio) |
| **Pandas** | Analyse de données |
| **Plotly** | Graphiques interactifs |
| **Supabase** | Base de données feedback |

---

## 📁 Structure du Projet

```
mercredi-translator/
│
├── app.py                          # 🎯 Application principale Streamlit
├── requirements.txt                # 📦 Dépendances Python
├── packages.txt                    # 📦 Dépendances système (Streamlit Cloud)
├── README.md                       # 📚 Cette documentation
│
├── .streamlit/
│   ├── config.toml                # ⚙️ Configuration Streamlit
│   └── secrets.toml               # 🔐 Secrets (non versionné)
│
├── modules/
│   ├── text_translator.py         # 📝 Traduction texte
│   ├── document_translator.py     # 📄 Traduction document
│   ├── audio_translator.py        # 🎙️ Transcription & traduction audio
│   ├── image_translator.py        # 🖼️ OCR & traduction image
│   ├── language_detector.py       # 🌍 Détection de langue
│   └── chatbot.py                 # 💬 Chatbot IA
│
├── .gitignore                      # Git ignore patterns

```

---

## 🔐 Configuration des Secrets

### .streamlit/secrets.toml
```toml
# Groq API (REQUIS)
GROQ_API_KEY = "gsk_YOUR_GROQ_KEY"

# OCR API (optionnel, par défaut "helloworld")
OCR_API_KEY = "YOUR_OCR_KEY"

# Supabase (optionnel pour feedback)
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-key"
```

> ⚠️ **IMPORTANT** : Ne commitez JAMAIS `secrets.toml` sur GitHub !
> Ajoutez-le à `.gitignore`

---

## 💡 Utilisation

### 1️⃣ Accéder à l'Application
1. Ouvrez https://mercredi-translator.streamlit.app
2. Entrez votre clé Groq API (gratuite)
3. Cliquez "Valider et commencer"

### 2️⃣ Traduire du Texte
- Sélectionnez les langues source/cible
- Entrez ou collez votre texte
- Cliquez "🔄 Traduire"
- Écoutez la traduction (bouton 🔊)

### 3️⃣ Traduire un Document
- Téléchargez un fichier (.txt, .docx, .pdf, .pptx)
- Choisissez la langue cible
- Cliquez "📄 Traduire"
- Téléchargez le document traduit

### 4️⃣ Transcrire de l'Audio
- Téléchargez un fichier audio
- Sélectionnez la langue cible
- Cliquez "🎙️ Transcrire & Traduire"
- Consultez les résultats

### 5️⃣ Extraire Texte d'Image
- Téléchargez une image
- Choisissez la langue cible
- Cliquez "🖼️ Extraire & Traduire"
- Lisez le texte traduit

### 6️⃣ Discuter avec le Chatbot
- Tapez votre question
- Attachez des images/documents si besoin
- Cliquez "💬" ou appuyez sur Entrée
- Écoutez les réponses

### 7️⃣ Consulter l'Historique
- Visualisez toutes vos traductions
- Exportez en `.txt`
- Videz l'historique si besoin

### 8️⃣ Donner un Feedback
- Évaluez chaque fonction
- Suggérez des améliorations
- Contributez à l'amélioration du produit

---

## 🎨 Design & UX

### Thème
- Design minimaliste Streamlit Native
- Responsive (mobile, tablet, desktop)

---

## 📊 Limites & Quotas

### API Groq (Gratuit)
- **100,000 tokens/jour**
- Modèles : Llama 3.3 70B, Whisper, etc.
- Créez un compte : https://console.groq.com

### OCR.space (Gratuit)
- **25 requests/jour** avec `OCR_API_KEY = "helloworld"`
- Optionnel pour OCR local via pytesseract

### Streamlit Cloud (Gratuit)
- **3 apps publiques**
- **1 GB RAM par app**
- Déploiement automatique depuis GitHub

---

## 🐛 Dépannage

### L'app ne démarre pas
```bash
# Vérifiez les dépendances
pip install -r requirements.txt

# Ou recréez l'environnement
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Erreur "GROQ_API_KEY not found"
1. Créez `.streamlit/secrets.toml`
2. Ou sur Streamlit Cloud : Settings → Secrets → Ajoutez vos clés

### OCR ne fonctionne pas
Sur Linux/Mac, installez tesseract :
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

### L'app est lente
- Utilisez `@st.cache_resource` pour les gros modèles
- Limitez les appels API simultanés
- Augmentez le RAM sur Streamlit Cloud (Pro)

---

## 🤝 Contribuer

Les contributions sont bienvenues ! 

### Comment contribuer
1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commitez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Amélioration souhaitées
- [ ] Support de plus de langues
- [ ] Traduction en temps réel (streaming)
- [ ] Collaboration multi-utilisateurs
- [ ] Sauvegarde dans le cloud
- [ ] API REST
- [ ] Applications mobile
- [ ] Intégration avec plus de services

---

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](./LICENSE) pour plus de détails.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 Support

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [OCR.space API](https://ocr.space/ocrapi)

### Aide
- 📧 Email : imaa9307@gmail.com


---

## 🙏 Remerciements

- **Groq** pour les modèles LLM gratuits et rapides
- **Streamlit** pour l'excellent framework
- **Communauté Open Source** pour toutes les dépendances

---

## 📈 Statistiques

- **⭐ Stars** : Aidez-nous en donnant une étoile !
- **👥 Contributeurs** : Rejoignez-nous !
- **📥 Forks** : Créez votre propre version !
- **💬 Discussions** : Partagez vos idées !



**Développé par Amina@2026**

