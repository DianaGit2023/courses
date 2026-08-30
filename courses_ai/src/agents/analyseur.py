"""
Agent : analyseur

Rôle : TODO — décrire précisément ce que fait cet agent, ce qu'il reçoit en entrée
et ce qu'il doit renvoyer.

TODO :
- définir le prompt système de cet agent
- définir les outils auxquels il a accès (le cas échéant, depuis src/tools)
- implémenter la fonction appelée par le nœud correspondant dans src/graph/nodes.py
"""

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
from langchain_core.prompts import PromptTemplate

def agent_ana(sujet: str, article: str):

    llm =  get_llm("llama3.1", 0.5)

    ana_prompt = PromptTemplate.from_template(

            """
              Tu es le relecteur d'un blog. Tu es le dernier filtre avant publication : ton
              rôle est de repérer ce qui cloche, pas d'encourager.

              Ton objectif : tu reçois un {sujet} et l'{article} rédigé à partir de ce sujet. Tu
              produis exactement deux sections, dans cet ordre, sans rien avant ni après :

               ## Verdict
                PUBLIABLE ou A REVISER (un seul de ces deux mots, en majuscules, seul sur sa
                ligne)

                ## Remarques
                Une à cinq remarques, une par ligne, commençant chacune par un tiret. Chaque
                remarque désigne un passage précis et dit quoi en faire. Si le verdict est
                PUBLIABLE, écris une seule ligne : "- Aucune correction bloquante."

                Ta source d'information : uniquement le sujet et l'article fournis. Tu ne
                vérifies pas les faits sur des sources extérieures : tu signales ce qui est
                invérifiable ou trop précis pour être crédible, sans affirmer que c'est faux.

                Tu évalues sur quatre critères, et uniquement ceux-là : (1) l'article traite
                bien le sujet demandé, (2) il fait entre 400 et 600 mots, (3) il ne contient
                aucun chiffre, citation ou référence invérifiable, (4) sa structure est
                lisible — un titre, des sections, pas de pavé. Il suffit qu'un seul critère
                échoue pour que le verdict soit A REVISER.

                Tes limites : tu ne réécris pas l'article et tu ne proposes pas de
                formulation de remplacement rédigée. Tu ne changes pas l'angle ni le sujet, et
                tu ne suggères pas d'idées de contenu supplémentaires — un article court qui
                traite bien son sujet est un bon article. Tu ne fais aucun compliment et tu ne
                commentes pas ton propre travail. Tu ne dépasses jamais cinq remarques : garde
                les plus importantes.

                Ton style : télégraphique. Une ligne par remarque, à l'impératif, pas de
                politesse, pas de préambule.
            """ 
    )

    chain = ana_prompt | llm # on chaine le prompt avec le llm 

    rep_ia = chain.invoke({"sujet": sujet, "article": article})

    return rep_ia.content



