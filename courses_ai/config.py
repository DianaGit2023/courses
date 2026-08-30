"""
Chargement de la configuration du projet à partir des variables d'environnement.

TODO :
- charger le .env avec python-dotenv
- exposer les constantes utilisées ailleurs dans le projet (OLLAMA_BASE_URL, OLLAMA_MODEL, ...)
- valider que les variables obligatoires sont bien présentes, sinon lever une erreur claire
"""

from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")



