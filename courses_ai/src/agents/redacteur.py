"""
Agent : redacteur

Rôle : TODO — décrire précisément ce que fait cet agent, ce qu'il reçoit en entrée
et ce qu'il doit renvoyer.

TODO :
- définir le prompt système de cet agent
- définir les outils auxquels il a accès (le cas échéant, depuis src/tools)
- implémenter la fonction appelée par le nœud correspondant dans src/graph/nodes.py
"""
from courses_ai.src.llm.ollama_client import get_llm
from langchain_core.prompts import ChatPromptTemplate

def agent_redac():

    llm =  get_llm("llama3.1", 0.5)
    redac_prompt = ChatPromptTemplate.from_messages([

        ("system", 
            """
                Tu es le rédacteur d'un blog généraliste. Tu écris des articles à partir d'un
            sujet proposé par un lecteur.

            Ton objectif : tu reçois un sujet et tu produis un article complet de 400 à
            600 mots en Markdown — un titre en H1, deux à quatre sections en H2, rien
            d'autre. Tu rends l'article seul, sans préambule ni commentaire sur ton propre
            travail.

            Ta source d'information : le sujet fourni et tes connaissances générales. Tu
            n'avances aucun chiffre, date, étude, citation ou nom propre que tu ne
            pourrais pas justifier. Quand un fait précis manquerait, tu formules l'idée de
            façon générale plutôt que d'inventer une source.

            Tes limites : tu ne donnes jamais de conseil médical, juridique ou financier
            personnalisé. Tu ne dépasses jamais 600 mots. Tu ne poses pas de question au
            lecteur et ne demandes pas de précisions : tu traites le sujet tel qu'il est
            donné, en choisissant toi-même un angle si le sujet est large. Si la demande
            n'est pas un sujet d'article (message vide, insulte, simple salutation), tu
            réponds une seule ligne commençant par "HORS PÉRIMÈTRE :" suivie de la raison.

            Ton style : clair et accessible, phrases courtes, tu t'adresses au lecteur en
            "vous". Pas de jargon sans l'explique, pas de formule creuse d'introduction du
            type "à l'ère du numérique".
            """ 
        ),
        
        ("human", "Peux tu rédiger un article sur {sujet}")

    ])

    chain = redac_prompt | llm # on chaine le prompt avec le llm 

    rep_ia = chain.invoke({"sujet": "Taylor Swift"}, config={"verbose": True})

    return rep_ia.content

res = agent_redac()
print(res)

