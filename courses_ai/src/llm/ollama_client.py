"""
Configuration du client Ollama utilisé par les agents.

TODO :
- instancier ChatOllama (langchain_ollama) avec OLLAMA_BASE_URL / OLLAMA_MODEL depuis config.py
- exposer une fonction get_llm() réutilisée par les agents
"""
from langchain_ollama import ChatOllama
from courses_ai.config import OLLAMA_BASE_URL

# Utilisation du llm en indiquant : modele choisi + temperature 
# Si déterministe 0 sinon proche de 1

def get_llm(nom_modele, temp):
    return ChatOllama(
            model=nom_modele,
            base_url=OLLAMA_BASE_URL,
            temperature=temp
)


