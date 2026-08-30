# """
# Point d'entrée Streamlit.

# TODO :
# - st.set_page_config(...)
# - construire / récupérer le graphe (src.graph.graph)
# - gérer l'état de session (historique de conversation, résultats intermédiaires...)
# - afficher les entrées utilisateur et les sorties du système multi-agents
# """
# """


import time

import streamlit as st

TONS = ["Intime", "Documenté", "Manifeste", "Guide pratique"]
FORMATS = ["Court · ~400 mots", "Standard · ~500 mots", "Long · ~600 mots"]

FAUX_TEXTE = (
    "<p>On croit photographier un objet. On photographie en réalité la manière dont "
    "la lumière le quitte. Le sujet n'est qu'un prétexte : ce qui compose une image, "
    "c'est l'endroit exact où le clair devient sombre.</p>"
    "<h3>Regarder plus lentement</h3>"
    "<p>Un même angle, à deux heures d'intervalle, donne deux images qui n'ont rien "
    "à se dire. La patience n'est pas une vertu ici, c'est une technique.</p>"
)

st.set_page_config(page_title="La Revue", page_icon="—", layout="centered")

# ── style ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&family=IBM+Plex+Mono&display=swap');
:root{ --ink:#0F0F0E; --graphite:#63635E; --rule:#E5E4E0; --wash:#F6F6F4; --accent:#2735CE; }

.stApp{ background:#fff; }
[data-testid="stHeader"]{ height:0; background:transparent; }
#MainMenu, footer, [data-testid="stToolbar"]{ display:none !important; }
.block-container{ max-width:840px !important; padding:0 32px 6rem !important; }
.stApp *{ font-family:'Source Serif 4',Georgia,serif; color:var(--ink); }

.mono{ font-family:'IBM Plex Mono',monospace !important; font-size:.66rem;
       letter-spacing:.14em; text-transform:uppercase; color:var(--graphite); }
.serif{ font-family:'Instrument Serif',serif !important; }

.masthead{ display:flex; justify-content:space-between; align-items:baseline; padding:2rem 0 .9rem; }
.masthead .name{ font-family:'Instrument Serif',serif !important; font-size:1.35rem; }
.masthead span{ margin-left:1.7rem; }
.double{ border-top:3px double var(--rule); }

.hero{ padding:3.4rem 0 3rem; }
.hero h1{ font-family:'Instrument Serif',serif !important; font-weight:400; margin:0;
          font-size:clamp(2.3rem,6vw,3.7rem); line-height:1.06; max-width:15ch; }
.hero em{ color:var(--accent); }
.hero p{ margin-top:1.4rem; max-width:46ch; font-size:1.05rem; line-height:1.62;
         color:var(--graphite); font-weight:300; }

.sec{ border-top:1px solid var(--rule); margin-top:2.8rem; padding-top:1.6rem; }
.gut .n{ font-family:'IBM Plex Mono',monospace !important; font-size:.66rem;
         letter-spacing:.14em; color:var(--accent); }
.gut .l{ font-family:'IBM Plex Mono',monospace !important; font-size:.66rem;
         letter-spacing:.14em; text-transform:uppercase; color:var(--graphite); margin-top:.4rem; }

.stTextInput label, .stSelectbox label{ font-family:'IBM Plex Mono',monospace !important;
  font-size:.62rem !important; letter-spacing:.14em; text-transform:uppercase;
  color:var(--graphite) !important; }
.stTextInput input{ background:#fff !important; border:1px solid var(--rule) !important;
  border-radius:2px !important; font-family:'Instrument Serif',serif !important;
  font-size:1.3rem !important; padding:.7rem .85rem !important; }
.stTextInput input:focus{ border-color:var(--accent) !important;
  box-shadow:0 0 0 3px rgba(39,53,206,.09) !important; }
[data-baseweb="select"] > div{ background:#fff !important; border:1px solid var(--rule) !important;
  border-radius:2px !important; font-family:'IBM Plex Mono',monospace !important;
  font-size:.7rem !important; min-height:44px; }

.stButton > button{ background:var(--accent); border:1px solid var(--accent); border-radius:2px;
  font-family:'IBM Plex Mono',monospace !important; font-size:.66rem; letter-spacing:.14em;
  text-transform:uppercase; padding:.95rem 1rem; width:100%; }
.stButton > button *{ color:#fff !important; }
.stButton > button:hover{ background:#1B27A8; border-color:#1B27A8; }
.stButton > button:disabled{ background:var(--wash); border-color:var(--rule); }
.stButton > button:disabled *{ color:#A7A7A1 !important; }

.steps{ display:flex; gap:.9rem; align-items:center; flex-wrap:wrap; }
.step{ display:flex; align-items:center; gap:.5rem; }
.dot{ width:6px; height:6px; border-radius:50%; border:1px solid var(--graphite); }
.step.on .dot{ background:var(--accent); border-color:var(--accent); }
.step.on .lb{ color:var(--accent); }
.step.done .dot{ background:var(--ink); border-color:var(--ink); }
.step.done .lb{ color:var(--ink); }
.lb{ font-family:'IBM Plex Mono',monospace !important; font-size:.66rem;
     letter-spacing:.14em; text-transform:uppercase; color:var(--graphite); }
.arrow{ color:var(--rule); }

.note{ margin-top:1.3rem; background:var(--wash); border-radius:2px; padding:1.1rem 1.3rem; }
.note .h{ font-family:'IBM Plex Mono',monospace !important; font-size:.62rem;
          letter-spacing:.14em; text-transform:uppercase; color:var(--accent); }
.note li{ font-size:.94rem; line-height:1.65; color:var(--graphite); }

.entry{ border-top:1px solid var(--rule); padding:2rem 0; }
.entry:last-child{ border-bottom:1px solid var(--rule); }
.entry summary{ list-style:none; cursor:pointer; display:grid;
                grid-template-columns:118px 1fr; gap:1.5rem; }
.entry summary::-webkit-details-marker{ display:none; }
.meta{ font-family:'IBM Plex Mono',monospace !important; font-size:.64rem; line-height:1.9;
       letter-spacing:.1em; text-transform:uppercase; color:var(--graphite); }
.kicker{ font-family:'IBM Plex Mono',monospace !important; font-size:.63rem;
         letter-spacing:.14em; text-transform:uppercase; color:var(--accent);
         display:block; margin-bottom:.6rem; }
.entry h2{ font-family:'Instrument Serif',serif !important; font-weight:400; margin:0;
           font-size:clamp(1.4rem,3.4vw,2rem); line-height:1.14; max-width:22ch; }
.entry summary:hover h2{ color:var(--accent); }
.lede{ margin-top:.7rem; font-size:1rem; line-height:1.68; color:var(--graphite);
       max-width:52ch; font-weight:300; }
.entry[open] .lede{ display:none; }
.prose{ margin:1.4rem 0 0 calc(118px + 1.5rem); max-width:62ch; }
.prose p{ font-size:1.1rem; line-height:1.78; margin:0 0 1.3rem; font-weight:300; }
.prose p:first-of-type:first-letter{ font-family:'Instrument Serif',serif; float:left;
  font-size:3.4rem; line-height:.86; padding:.1rem .5rem 0 0; color:var(--accent); }
.prose h3{ font-family:'IBM Plex Mono',monospace !important; font-size:.66rem;
  letter-spacing:.14em; text-transform:uppercase; color:var(--graphite);
  margin:2.2rem 0 1rem; font-weight:400; }
.empty{ border-top:1px solid var(--rule); border-bottom:1px solid var(--rule); padding:3rem 0; }
.empty p{ font-family:'Instrument Serif',serif !important; font-size:1.3rem;
          color:var(--graphite); margin:0; }
@media (max-width:640px){ .entry summary{ grid-template-columns:1fr; } .prose{ margin-left:0; } }
</style>
""",
    unsafe_allow_html=True,
)


def gutter(num, label):
    return f'<div class="gut"><div class="n">{num}</div><div class="l">{label}</div></div>'


def steps(etats):
    out = []
    for i, nom in enumerate(["Rédaction", "Relecture", "Publication"]):
        if i:
            out.append('<span class="arrow">→</span>')
        out.append(
            f'<span class="step {etats.get(nom, "")}"><span class="dot"></span>'
            f'<span class="lb">{nom}</span></span>'
        )
    return f'<div class="steps">{"".join(out)}</div>'


# ── état ─────────────────────────────────────────────────────────────────────
if "articles" not in st.session_state:
    st.session_state.articles = []

# ── manchette + chapeau ──────────────────────────────────────────────────────
st.markdown(
    '<div class="masthead"><div class="name">La Revue</div>'
    '<div class="mono"><span>Écrire</span><span>Fabrique</span><span>Archive</span></div></div>'
    '<div class="double"></div>'
    "<div class=\"hero\"><h1>Proposez un sujet.<br>On vous écrit <em>l'article</em>.</h1>"
    "<p>Un modèle rédige, un second le relit et tranche. "
    "Ce qui passe la relecture est publié ci-dessous.</p></div>",
    unsafe_allow_html=True,
)

# ── 01 · le sujet ────────────────────────────────────────────────────────────
st.markdown('<div class="sec"></div>', unsafe_allow_html=True)
g, c = st.columns([1, 3.4], gap="medium")
with g:
    st.markdown(gutter("01", "Le sujet"), unsafe_allow_html=True)
with c:
    sujet = st.text_input(
        "De quoi voulez-vous lire un article ?",
        placeholder="Pourquoi les vieilles recettes n'ont jamais de grammes",
    )
    a, b, d = st.columns([1.2, 1.2, 1])
    ton = a.selectbox("Ton", TONS)
    fmt = b.selectbox("Longueur", FORMATS)
    d.markdown('<div style="height:1.62rem"></div>', unsafe_allow_html=True)
    lancer = d.button("Écrire l'article", disabled=not sujet.strip())

# ── 02 · la fabrique ─────────────────────────────────────────────────────────
st.markdown('<div class="sec"></div>', unsafe_allow_html=True)
g, c = st.columns([1, 3.4], gap="medium")
with g:
    st.markdown(gutter("02", "La fabrique"), unsafe_allow_html=True)
with c:
    scene = st.empty()
    retour = st.empty()

if not lancer:
    scene.markdown(steps({}), unsafe_allow_html=True)
else:
    for etats in (
        {"Rédaction": "on"},
        {"Rédaction": "done", "Relecture": "on"},
        {"Rédaction": "done", "Relecture": "done", "Publication": "done"},
    ):
        scene.markdown(steps(etats), unsafe_allow_html=True)
        time.sleep(0.9)

    retour.markdown(
        '<div class="note"><div class="h">Note du rédacteur en chef — 8/10</div><ul>'
        "<li>L'accroche tarde de deux paragraphes.</li>"
        "<li>Le troisième exemple répète le premier.</li></ul></div>",
        unsafe_allow_html=True,
    )
    st.session_state.articles.insert(
        0,
        {
            "titre": "Ce que la lumière fait aux choses",
            "sujet": sujet.strip(),
            "ton": ton,
            "date": "29 août 2026",
            "lecture": 2,
            "lede": "On croit photographier un objet. On photographie en réalité la "
            "manière dont la lumière le quitte…",
        },
    )

# ── 03 · l'archive ───────────────────────────────────────────────────────────
st.markdown('<div class="sec"></div>', unsafe_allow_html=True)
g, c = st.columns([1, 3.4], gap="medium")
with g:
    st.markdown(gutter("03", "L'archive"), unsafe_allow_html=True)
with c:
    st.markdown(
        f'<div class="mono">{len(st.session_state.articles)} article(s) publié(s)</div>',
        unsafe_allow_html=True,
    )

if st.session_state.articles:
    total = len(st.session_state.articles)
    entries = "".join(
        f"""
        <details class="entry">
          <summary>
            <div class="meta">Nº {total - i:03d}<br>{a['date']}<br>{a['lecture']} min de lecture<br>Relecture 8/10</div>
            <div>
              <span class="kicker">{a['ton']} &nbsp;·&nbsp; {a['sujet']}</span>
              <h2>{a['titre']}</h2>
              <p class="lede">{a['lede']}</p>
            </div>
          </summary>
          <div class="prose">{FAUX_TEXTE}</div>
        </details>
        """
        for i, a in enumerate(st.session_state.articles)
    )
    st.markdown(f'<div style="margin-top:1.4rem">{entries}</div>', unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="empty" style="margin-top:1.4rem">'
        "<p>Le premier sujet ouvre l'archive.</p></div>",
        unsafe_allow_html=True,
    )