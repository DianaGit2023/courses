# courses_ai

Système multi-agents (LangGraph + Ollama) piloté par une interface Streamlit.

## Structure

- `app.py` — point d'entrée Streamlit
- `config.py` — chargement de la config / variables d'environnement
- `src/graph/` — état, nœuds et graphe LangGraph
- `src/agents/` — un fichier par agent
- `src/tools/` — outils partagés entre agents
- `src/llm/` — client Ollama / configuration du modèle
- `tests/` — tests unitaires

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env       # puis remplir .env
```

## Lancer l'app

```bash
streamlit run app.py
```

## TODO

- [ ] Définir le `State` du graphe (`src/graph/state.py`)
- [ ] Implémenter les nœuds (`src/graph/nodes.py`)
- [ ] Construire le graphe (`src/graph/graph.py`)
- [ ] Implémenter chaque agent (`src/agents/`)
- [ ] Brancher le graphe à l'UI Streamlit (`app.py`)
