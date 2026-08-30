"""
Construction du graphe LangGraph : ajout des nœuds, arêtes, routage conditionnel.

TODO :
- instancier StateGraph(State)
- ajouter les nœuds (import depuis nodes.py)
- définir les arêtes (séquentielles et/ou conditionnelles selon le routage voulu)
- compiler le graphe et l'exposer (fonction get_graph() par exemple)
"""

from langgraph.graph import StateGraph, START, END

from courses_ai.src.graph.state import BlogState
from courses_ai.src.graph.nodes import node_redacteur, node_analyseur

MAX_TOURS = 3


def apres_analyse(state: BlogState) -> str:
    if state["verdict"] == "PUBLIABLE":
        return "fin"
    if state["tours"] >= MAX_TOURS:
        return "fin"
    return "reecrire"


def build_graph():
    workflow = StateGraph(BlogState)

    workflow.add_node("redacteur", node_redacteur)
    workflow.add_node("analyseur", node_analyseur)

    workflow.add_edge(START, "redacteur")
    workflow.add_edge("redacteur", "analyseur")

    workflow.add_conditional_edges(
        "analyseur",
        apres_analyse,
        {"reecrire": "redacteur", "fin": END},
    )

    return workflow.compile()