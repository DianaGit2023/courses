"""
Nœuds du graphe : chaque fonction prend le State en entrée et retourne
les champs du State à mettre à jour.

TODO :
- un nœud par étape / agent du pipeline
- gérer les erreurs et les cas où un agent ne renvoie rien d'exploitable
"""

from courses_ai_ai.src.agents.redacteur import agent_redac
from courses_ai_ai.src.agents.analyseur import agent_ana


def node_redacteur(state: BlogState) -> dict:
    article = agent_red(
        sujet=state["sujet"],
        remarques=state.get("remarques", ""),   # vide au 1er tour
    )
    return {"article": article, "tours": state.get("tours", 0) + 1}


def node_analyseur(state: BlogState) -> dict:
    retour = agent_ana(sujet=state["sujet"], article=state["article"])

    verdict = "A REVISER"
    if "PUBLIABLE" in retour.upper():
        verdict = "PUBLIABLE"

    return {"verdict": verdict, "remarques": retour}

