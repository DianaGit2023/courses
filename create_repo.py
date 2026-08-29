#!/usr/bin/env python3
"""
Générateur de squelette de repo : système multi-agents avec Streamlit, LangChain/LangGraph et Ollama.

Usage :
    python create_repo.py mon-projet
    python create_repo.py mon-projet --path C:\\dev
    python create_repo.py mon-projet --agents collecteur,analyseur,redacteur

Le script crée uniquement la structure et des fichiers squelettes (docstrings + TODO).
Aucune logique métier n'est écrite dans les fichiers — c'est fait exprès, à toi de remplir.
"""

import argparse
import sys
from pathlib import Path

DEFAULT_AGENTS = ["example_agent"]


def w(path: Path, content: str = "") -> None:
    """Écrit un fichier, en créant les dossiers parents si besoin."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  créé : {path}")


def build(root: Path, agents: list[str]) -> None:
    project = root

    # --- fichiers racine -------------------------------------------------
    w(project / ".env.example", """\
# Copie ce fichier en .env et remplis les valeurs — ne jamais commit .env

# Ollama (local ou serveur d'inférence distant)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Optionnel — tracing / observabilité LangSmith
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=
# LANGCHAIN_PROJECT=

# Optionnel — si un agent appelle une API externe (ajouter au besoin)
# EXAMPLE_API_KEY=
""")

    w(project / ".gitignore", """\
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Env / secrets
.env

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Data / logs (à ajuster selon le projet)
*.log
/data/raw/
""")

    w(project / "requirements.txt", """\
streamlit
langchain
langchain-community
langgraph
langchain-ollama
python-dotenv
pytest
""")

    w(project / "README.md", f"""\
# {project.name}

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
.venv\\Scripts\\activate   # Windows
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
""")

    w(project / "config.py", '''\
"""
Chargement de la configuration du projet à partir des variables d'environnement.

TODO :
- charger le .env avec python-dotenv
- exposer les constantes utilisées ailleurs dans le projet (OLLAMA_BASE_URL, OLLAMA_MODEL, ...)
- valider que les variables obligatoires sont bien présentes, sinon lever une erreur claire
"""

# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
''')

    w(project / "app.py", '''\
"""
Point d'entrée Streamlit.

TODO :
- st.set_page_config(...)
- construire / récupérer le graphe (src.graph.graph)
- gérer l'état de session (historique de conversation, résultats intermédiaires...)
- afficher les entrées utilisateur et les sorties du système multi-agents
"""
''')

    # --- src/graph ---------------------------------------------------------
    w(project / "src" / "__init__.py")

    w(project / "src" / "graph" / "__init__.py")

    w(project / "src" / "graph" / "state.py", '''\
"""
Définition du State partagé entre les nœuds du graphe LangGraph.

TODO :
- définir une classe (TypedDict ou pydantic BaseModel) représentant l'état :
  entrée utilisateur, résultats de chaque agent, historique, décisions de routage...
"""
''')

    w(project / "src" / "graph" / "nodes.py", '''\
"""
Nœuds du graphe : chaque fonction prend le State en entrée et retourne
les champs du State à mettre à jour.

TODO :
- un nœud par étape / agent du pipeline
- gérer les erreurs et les cas où un agent ne renvoie rien d'exploitable
"""
''')

    w(project / "src" / "graph" / "graph.py", '''\
"""
Construction du graphe LangGraph : ajout des nœuds, arêtes, routage conditionnel.

TODO :
- instancier StateGraph(State)
- ajouter les nœuds (import depuis nodes.py)
- définir les arêtes (séquentielles et/ou conditionnelles selon le routage voulu)
- compiler le graphe et l'exposer (fonction get_graph() par exemple)
"""
''')

    # --- src/agents ---------------------------------------------------------
    w(project / "src" / "agents" / "__init__.py")

    for agent in agents:
        w(project / "src" / "agents" / f"{agent}.py", f'''\
"""
Agent : {agent}

Rôle : TODO — décrire précisément ce que fait cet agent, ce qu'il reçoit en entrée
et ce qu'il doit renvoyer.

TODO :
- définir le prompt système de cet agent
- définir les outils auxquels il a accès (le cas échéant, depuis src/tools)
- implémenter la fonction appelée par le nœud correspondant dans src/graph/nodes.py
"""
''')

    # --- src/tools ---------------------------------------------------------
    w(project / "src" / "tools" / "__init__.py")
    w(project / "src" / "tools" / "tools.py", '''\
"""
Outils partagés, utilisables par un ou plusieurs agents (via @tool de LangChain).

TODO :
- définir chaque outil avec le décorateur @tool et une docstring claire
  (la docstring sert de description à l'agent — elle doit être précise)
"""
''')

    # --- src/llm ---------------------------------------------------------
    w(project / "src" / "llm" / "__init__.py")
    w(project / "src" / "llm" / "ollama_client.py", '''\
"""
Configuration du client Ollama utilisé par les agents.

TODO :
- instancier ChatOllama (langchain_ollama) avec OLLAMA_BASE_URL / OLLAMA_MODEL depuis config.py
- exposer une fonction get_llm() réutilisée par les agents
"""
''')

    # --- src/ui (composants Streamlit réutilisables) ------------------------
    w(project / "src" / "ui" / "__init__.py")
    w(project / "src" / "ui" / "components.py", '''\
"""
Composants Streamlit réutilisables (affichage des résultats, historique, etc.).

TODO :
- fonctions d'affichage appelées depuis app.py, pour ne pas surcharger app.py
"""
''')

    # --- tests -------------------------------------------------------------
    w(project / "tests" / "__init__.py")
    w(project / "tests" / "test_tools.py", '''\
"""
Tests unitaires pour src/tools/tools.py.

TODO : un test par outil (cas nominal + cas limite).
"""
''')

    print(f"\n✅ Repo créé dans : {project.resolve()}")
    print(f"   Agents créés : {', '.join(agents)}")
    print("\nProchaines étapes :")
    print(f"  cd {project}")
    print("  python -m venv .venv && .venv\\Scripts\\activate  (Windows)")
    print("  pip install -r requirements.txt")
    print("  cp .env.example .env")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Nom du projet / du dossier à créer")
    parser.add_argument("--path", default=".", help="Dossier parent où créer le projet (défaut : dossier courant)")
    parser.add_argument(
        "--agents",
        default=",".join(DEFAULT_AGENTS),
        help="Liste d'agents séparés par des virgules, ex: collecteur,analyseur,redacteur",
    )
    args = parser.parse_args()

    root = Path(args.path) / args.name
    if root.exists() and any(root.iterdir()):
        print(f"❌ Le dossier {root} existe déjà et n'est pas vide. Choisis un autre nom ou vide-le d'abord.")
        sys.exit(1)

    agents = [a.strip() for a in args.agents.split(",") if a.strip()]
    build(root, agents)


if __name__ == "__main__":
    main()
