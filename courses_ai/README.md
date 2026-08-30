<div align="center">

# 📰 La Revue

**Proposez un sujet. On vous écrit l'article.**

Un modèle rédige, un second le relit et tranche.
Ce qui passe la relecture est publié.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

</div>

---

## ✨ Le principe

Vous donnez un sujet, un ton et une longueur. Le **rédacteur** écrit l'article, l'**analyseur** le relit et décide : soit il renvoie le texte en réécriture avec ses remarques, soit il le laisse passer et l'article rejoint l'archive.

```
              📝 Sujet + ton + longueur
                        │
                        ▼
                 ✍️  redacteur
                        │  ▲
                        ▼  │ ↩︎ à retravailler
                 🔍 analyseur
                        │
                        │ ✅ validé
                        ▼
                 📚 Publication
```

Tout tourne en local : le modèle est servi par **Ollama**, l'orchestration par **LangGraph**, l'interface par **Streamlit**.

---

## 🖥️ L'interface

| Onglet | Ce qu'on y fait |
|:--|:--|
| ✍️ **Écrire** | `01 · Le sujet` — de quoi voulez-vous lire un article ? Ton et longueur au choix. |
| 🏭 **Fabrique** | `02 · La fabrique` — le cycle Rédaction → Relecture → Publication en direct. |
| 📚 **Archive** | `03 · L'archive` — tous les articles qui ont passé la relecture. |

> 💡 Format des articles : 400-600 mots, en Markdown.

---

## 🕸️ Le graphe

```python
__start__ ──► redacteur ──► analyseur ──┬──► redacteur   # relecture négative
                                        └──► __end__     # article validé
```

Deux nœuds, une boucle conditionnelle : l'analyseur est le seul à pouvoir mettre fin à la partie.

---

## 📁 Structure du projet

```
courses_ai/
├── 🚀 app.py              # Point d'entrée Streamlit
├── ⚙️  config.py           # Chargement de la config / variables d'environnement
├── 🕸️  langgraph.json      # Déclaration du graphe pour LangGraph Studio
├── 📋 requirements.txt
├── 🔐 .env.example        # Modèle de configuration à copier en .env
├── 📦 src/
│   ├── 🕸️  graph/          # État, nœuds et graphe LangGraph
│   ├── 🤖 agents/         # redacteur, analyseur
│   ├── 🔧 tools/          # Outils partagés entre agents
│   ├── 🦙 llm/            # Client Ollama / configuration du modèle
│   └── 🎨 ui/             # Composants et mise en page Streamlit
└── 🧪 tests/              # Tests unitaires
```

---

## 🔧 Installation

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env         # puis remplir .env
```

> 💡 Sur macOS / Linux : `source .venv/bin/activate`.
> ⚠️ Ollama doit tourner en local avant de lancer l'app.

---

## ▶️ Lancer l'app

```bash
ollama serve        # si ce n'est pas déjà le cas
streamlit run app.py
```

### 🔬 Inspecter le graphe

Le fichier `langgraph.json` permet d'ouvrir le graphe dans LangGraph Studio, pour suivre les allers-retours entre le rédacteur et l'analyseur pas à pas :

```bash
langgraph dev
```

---

## 🗺️ Roadmap

| | Étape |
|:--:|:--|
| ✅ | Définir le `State` du graphe |
| ✅ | Nœuds `redacteur` et `analyseur` |
| ✅ | Boucle conditionnelle de relecture |
| ✅ | Interface Streamlit (Écrire / Fabrique / Archive) |
| ⬜ | Persistance de l'archive entre deux sessions |
| ⬜ | Limiter le nombre d'allers-retours de relecture |

<sub>✅ = fait · 🚧 = en cours · ⬜ = à faire</sub>

---

<div align="center">

Écrit par une machine, relu par une autre. ☕

</div>