"""
Nœuds du graphe : chaque fonction prend le State en entrée et retourne
les champs du State à mettre à jour.
"""

from src.agents.redacteur import agent_redac
from src.agents.analyseur import agent_ana
from src.graph.state import BlogState


def node_redacteur(state: BlogState) -> dict:
    iteration = state.get("iterations", 0)
    print(f"[redacteur] iteration={iteration}")

    try:
        article = agent_redac(
            sujet=state["sujet"],
            article=state.get("article", ""),      # vide au 1er tour
            critique=state.get("critique", ""),    # vide au 1er tour
        )
    except Exception as e:
        return {"critique": f"Erreur rédacteur : {e}", "valide": True}

    if not article or not article.strip():
        return {"critique": "Le rédacteur n'a rien renvoyé.", "valide": True}

    if article.lstrip().startswith("HORS PÉRIMÈTRE"):
        return {"article": article, "valide": True}

    return {"article": article}


def node_analyseur(state: BlogState) -> dict:
    iteration = state.get("iterations", 0)
    print(f"[analyseur] iteration={iteration}")

    try:
        retour = agent_ana(sujet=state["sujet"], article=state["article"])
    except Exception as e:
        return {"critique": f"Erreur analyseur : {e}", "valide": True}

    valide = "PUBLIABLE" in retour.upper()

    return {
        "critique": retour,
        "valide": valide,
        "iterations": iteration + 1,
    }