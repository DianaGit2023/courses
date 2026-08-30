from src.graph.graph import build_graph

app = build_graph()

resultat = app.invoke({
    "sujet": "Les bienfaits de la marche en montagne",
    "article": "",
    "verdict": "",
    "remarques": "",
    "tours": 0,
})

print(resultat["valide"])
print(resultat["critique"])
print(resultat["article"])