"""
Composants Streamlit réutilisables (affichage des résultats, historique, etc.).

TODO :
- fonctions d'affichage appelées depuis app.py, pour ne pas surcharger app.py
"""
"""
Composants Streamlit réutilisables : mise en forme et extraction.

Aucun de ces composants ne connaît LangGraph. Ils reçoivent des chaînes de
caractères et renvoient du HTML ou du texte, rien de plus.
"""

import html
import re

MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]

ETAPES = ["Rédaction", "Relecture", "Publication"]


# ── mise en forme ────────────────────────────────────────────────────────────

def gutter(num: str, label: str) -> str:
    """Le numéro et le libellé de section dans la colonne de gauche."""
    return f'<div class="gut"><div class="n">{num}</div><div class="l">{label}</div></div>'


def steps(etats: dict) -> str:
    """La frise Rédaction → Relecture → Publication.

    etats : {"Rédaction": "done", "Relecture": "on"} — les clés absentes
    restent au repos.
    """
    out = []
    for i, nom in enumerate(ETAPES):
        if i:
            out.append('<span class="arrow">→</span>')
        out.append(
            f'<span class="step {etats.get(nom, "")}"><span class="dot"></span>'
            f'<span class="lb">{nom}</span></span>'
        )
    return f'<div class="steps">{"".join(out)}</div>'


def date_fr(dt) -> str:
    return f"{dt.day} {MOIS[dt.month - 1]} {dt.year}"


def compter_mots(texte: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ'-]+\b", texte))


def temps_lecture(texte: str) -> int:
    """Minutes de lecture, à 200 mots/minute, minimum 1."""
    return max(1, round(compter_mots(texte) / 200))


# ── lecture de l'article ─────────────────────────────────────────────────────

def extraire_titre(article: str, defaut: str = "Sans titre") -> str:
    """Le premier titre H1 du Markdown, sinon la première ligne non vide."""
    for ligne in article.splitlines():
        ligne = ligne.strip()
        if ligne.startswith("# "):
            return ligne[2:].strip()
    for ligne in article.splitlines():
        if ligne.strip():
            return ligne.strip().lstrip("#").strip()
    return defaut


def extraire_lede(article: str, limite: int = 150) -> str:
    """Le premier paragraphe de l'article, tronqué."""
    for ligne in article.splitlines():
        ligne = ligne.strip()
        if ligne and not ligne.startswith("#"):
            if len(ligne) <= limite:
                return ligne
            return ligne[:limite].rsplit(" ", 1)[0] + "…"
    return ""


def markdown_vers_html(article: str, ignorer_h1: bool = True) -> str:
    """Convertit le Markdown produit par le rédacteur en HTML.

    Streamlit ne rend pas le Markdown à l'intérieur d'un bloc HTML brut, il
    faut donc convertir soi-même. Le rédacteur ne produit que des titres, des
    paragraphes et parfois des listes : pas besoin d'une bibliothèque.
    """
    sortie: list[str] = []
    paragraphe: list[str] = []

    def vider_paragraphe() -> None:
        if paragraphe:
            texte = html.escape(" ".join(paragraphe))
            texte = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texte)
            texte = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", texte)
            sortie.append(f"<p>{texte}</p>")
            paragraphe.clear()

    for ligne in article.splitlines():
        ligne = ligne.strip()

        if not ligne:
            vider_paragraphe()
        elif ligne.startswith("#"):
            vider_paragraphe()
            niveau = len(ligne) - len(ligne.lstrip("#"))
            titre = html.escape(ligne.lstrip("#").strip())
            if niveau == 1 and ignorer_h1:
                continue  # le H1 est déjà affiché comme titre de l'entrée
            sortie.append(f"<h3>{titre}</h3>")
        elif ligne.startswith(("- ", "* ")):
            vider_paragraphe()
            sortie.append(f'<p class="puce">{html.escape(ligne[2:].strip())}</p>')
        else:
            paragraphe.append(ligne)

    vider_paragraphe()
    return "".join(sortie)


# ── lecture de la critique ───────────────────────────────────────────────────

def extraire_remarques(critique: str) -> list[str]:
    """Les lignes commençant par un tiret, après la section Remarques."""
    remarques = []
    for ligne in critique.splitlines():
        ligne = ligne.strip()
        if ligne.startswith(("- ", "– ", "— ", "* ")):
            remarques.append(ligne[2:].strip())
    return remarques


def bloc_note(critique: str, valide: bool, iterations: int) -> str:
    """L'encadré « Note du relecteur » affiché sous la frise."""
    verdict = "Publiable" if valide else "À réviser"
    passages = "1 relecture" if iterations <= 1 else f"{iterations} relectures"
    entete = f"Note du relecteur — {verdict} · {passages}"

    remarques = extraire_remarques(critique)
    if remarques:
        items = "".join(f"<li>{html.escape(r)}</li>" for r in remarques[:5])
    else:
        # l'agent n'a pas suivi le format attendu : on montre le texte brut
        items = f"<li>{html.escape(critique.strip()[:400])}</li>"

    return f'<div class="note"><div class="h">{entete}</div><ul>{items}</ul></div>'


def bloc_message(titre: str, texte: str) -> str:
    """Encadré neutre : hors périmètre, erreur d'agent, etc."""
    return (
        f'<div class="note"><div class="h">{html.escape(titre)}</div>'
        f'<ul><li>{html.escape(texte.strip()[:400])}</li></ul></div>'
    )


# ── archive ──────────────────────────────────────────────────────────────────

def carte_article(a: dict, numero: int) -> str:
    """Une entrée dépliable de l'archive."""
    verdict = "Publiable" if a["valide"] else "À réviser"
    return f"""
    <details class="entry">
      <summary>
        <div class="meta">Nº {numero:03d}<br>{a['date']}<br>{a['lecture']} min de lecture<br>{verdict}</div>
        <div>
          <span class="kicker">{html.escape(a['ton'])} &nbsp;·&nbsp; {html.escape(a['sujet'])}</span>
          <h2>{html.escape(a['titre'])}</h2>
          <p class="lede">{html.escape(a['lede'])}</p>
        </div>
      </summary>
      <div class="prose">{a['corps']}</div>
    </details>
    """