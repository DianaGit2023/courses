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
    if state.get("valide") or state.get("iterations", 0) >= 3:
        return "fin"
    return "reecriture"

    
def build_graph():
    workflow = StateGraph(BlogState)

    workflow.add_node("redacteur", node_redacteur)
    workflow.add_node("analyseur", node_analyseur)

    workflow.add_edge(START, "redacteur")
    workflow.add_edge("redacteur", "analyseur")

    workflow.add_conditional_edges(
        "analyseur",
        apres_analyse,
        {"fin": END, "reecriture": "redacteur"},
    )

    return workflow.compile()