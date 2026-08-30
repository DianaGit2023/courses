"""
Définition du State partagé entre les nœuds du graphe LangGraph.

TODO :
- définir une classe (TypedDict ou pydantic BaseModel) représentant l'état :
  entrée utilisateur, résultats de chaque agent, historique, décisions de routage...
"""
from typing import TypedDict, List

class BlogState(TypedDict):
    sujet: str             # Le sujet initial donné par l'utilisateur
    article: str           # Le texte de l'article (mis à jour par le Rédacteur)
    critique: str          # Les commentaires et corrections (fournis par le Critique)
    iterations: int        # Un compteur pour éviter les boucles infinies
    valide: bool           # Le signal d'arrêt (True = fini, False = on continue)


