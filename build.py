# -*- coding: utf-8 -*-
"""
Generateur de la maquette « Football All-in-One ».

Les pages sont GENEREES. Ne jamais modifier un .html a la main : la
modification serait ecrasee a la generation suivante, et la version corrigee
serait celle que personne ne regarde.

  python3 build.py     -> ecrit les .html a cote de ce fichier
"""
import html
import json
import os

from donnees import (BASELINE, COMPETITIONS, DONNEES, LIGUE, MARQUE, POSTES,
                     PAYS, PIEDS, VIDE)

RACINE = os.path.dirname(os.path.abspath(__file__))
VERSION_CSS = 3          # a incrementer a CHAQUE modification de assets/site.css

E = html.escape


def tbd():
    return f'<span class="tbd">{VIDE}</span>'


BALLON = ('<svg class="bal" viewBox="0 0 32 32" aria-hidden="true">'
          '<circle cx="16" cy="16" r="14" fill="none" stroke="#25D07A" stroke-width="2"/>'
          '<path d="M16 7l5.5 4-2.1 6.5h-6.8L10.5 11z" fill="#25D07A"/>'
          '</svg>')

MENU = [
    ("index.html", "Home"),
    ("live.html", "Live scores"),
    ("players.html", "Players"),
    ("clubs.html", "Clubs"),
    ("recruitment.html", "Recruitment"),
    ("data.html", "About the data"),
]


def page(fichier, titre, description, corps, actuel=None):
    nav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == (actuel or fichier) else ""}>{E(t)}</a>'
        for f, t in MENU)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titre)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="assets/site.css?v={VERSION_CSS}">
</head>
<body>

<div class="avert"><div class="wrap">
  <b>Mockup.</b> Every club, player, match and figure on this site is invented.
  Nothing here is real football data, and nothing is claimed about any real
  person or club &mdash; <a href="data.html">what a live version would need</a>.
</div></div>

<header class="top"><div class="wrap bar">
  <a class="marque" href="index.html">{BALLON}<span>{E(MARQUE)}</span></a>
  <nav class="nav">{nav}</nav>
</div></header>

<main>
{corps}
</main>

<footer class="pied"><div class="wrap">
  {E(MARQUE)} &mdash; working mockup, {E(BASELINE.lower())}.
  No real data, no account, no payment, no tracker.
  <a href="data.html">About the data</a>.
</div></footer>

</body>
</html>
"""
    chemin = os.path.join(RACINE, fichier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"  {fichier:<22} {len(doc):>7} o")


def ecu(couleur, code):
    return (f'<span class="ecu" style="background:{couleur}" aria-hidden="true"></span>'
            f'<span>{E(code)}</span>')


def club_par_slug(slug):
    return [c for c in DONNEES["clubs"] if c["slug"] == slug][0]


def bloc_match(m, lien=True):
    dom = club_par_slug(m["domicile_slug"])
    ext = club_par_slug(m["exterieur_slug"])
    if m["etat"] == "live":
        etat = f'<span class="etat live"><span class="pt"></span>{m["minute"]}\''
        etat += "</span>"
    elif m["etat"] == "termine":
        etat = '<span class="etat">FT</span>'
    else:
        etat = f'<span class="etat">{E(m["heure"])}</span>'
    if m["score_dom"] is None:
        score = '<div class="sc vide">&ndash;</div>'
    else:
        score = f'<div class="sc">{m["score_dom"]}&ndash;{m["score_ext"]}</div>'
    return f"""<a class="match" href="club-{E(m['domicile_slug'])}.html" data-etat="{m['etat']}">
  {etat}
  <div class="equipes">
    <div class="eq">{ecu(dom['couleur'], dom['nom'])}</div>
    <div class="eq">{ecu(ext['couleur'], ext['nom'])}</div>
  </div>
  {score}
</a>"""


def initiales(nom):
    bouts = nom.split()
    return (bouts[0][0] + bouts[-1][0]).upper()


def couleur_club(slug):
    return club_par_slug(slug)["couleur"]


# ===========================================================================
# 1. ACCUEIL
def accueil():
    live = [m for m in DONNEES["matchs"] if m["etat"] == "live"]
    a_venir = [m for m in DONNEES["matchs"] if m["etat"] == "avenir"][:3]
    top = sorted(DONNEES["joueurs"], key=lambda j: (-j["buts"], -j["passes"]))[:5]
    dispo = sum(1 for j in DONNEES["joueurs"] if j["disponible"])

    lignes_top = "".join(
        f'<tr><td class="pos">{i}</td>'
        f'<td><a href="player-{E(j["slug"])}.html" style="text-decoration:none">{E(j["nom"])}</a></td>'
        f'<td style="color:var(--gris)">{E(j["club"])}</td>'
        f'<td class="n">{j["buts"]}</td><td class="n">{j["passes"]}</td></tr>'
        for i, j in enumerate(top, start=1))

    return f"""
<section class="sec"><div class="wrap">
  <h1>Football &mdash; everything in one place</h1>
  <p class="chapeau">Live scores, player and club profiles, and a recruitment
  marketplace where clubs post what they are looking for and players apply.
  This page is a working mockup of that product: you can filter, search and
  open every profile. The data behind it is invented.</p>
  <div class="actions">
    <a class="btn" href="recruitment.html">Open the recruitment search</a>
    <a class="btn btn-b" href="data.html">What a live version needs</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>Live now</h2><a class="plus" href="live.html">All matches &rarr;</a></div>
  {''.join(bloc_match(m) for m in live)}
</div></section>

<section class="sec"><div class="wrap">
  <div class="grille g2">
    <div>
      <div class="sec-h"><h2>Top scorers</h2><a class="plus" href="players.html">All players &rarr;</a></div>
      <div class="enroule"><table class="tab">
        <thead><tr><th class="pos"></th><th>Player</th><th>Club</th>
        <th class="n">G</th><th class="n">A</th></tr></thead>
        <tbody>{lignes_top}</tbody>
      </table></div>
    </div>
    <div>
      <div class="sec-h"><h2>Upcoming</h2></div>
      {''.join(bloc_match(m) for m in a_venir)}
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>The rest of the platform</h2></div>
  <div class="grille g4">
    <div class="carte"><h3>Recruitment</h3>
      <p><b style="color:var(--vert);font-family:var(--mono)">{dispo}</b> players
      listed as available in this mockup, filterable by fourteen criteria.</p></div>
    <div class="carte"><h3>Transfers</h3>
      <p>{tbd()}<br>A transfer database is a licensed feed, not something a site
      can compile on its own.</p></div>
    <div class="carte"><h3>Videos</h3>
      <p>{tbd()}<br>Match highlights are broadcast rights. A player's own videos
      are a different question, and that part can be built.</p></div>
    <div class="carte"><h3>Shop</h3>
      <p>{tbd()}<br>Selling club kit needs a licence from the club or the brand.</p></div>
  </div>
</div></section>
"""


# ===========================================================================
# 2. SCORES
def scores():
    onglets = [("all", "All"), ("live", "Live"), ("termine", "Finished"),
               ("avenir", "Upcoming")]
    boutons = "".join(
        f'<button class="onglet" type="button" data-f="{k}"'
        f'{" aria-pressed=\"true\"" if k == "all" else " aria-pressed=\"false\""}>{E(l)}</button>'
        for k, l in onglets)
    return f"""
<section class="sec"><div class="wrap">
  <h1>Live scores</h1>
  <p class="chapeau">The four states the brief asks for &mdash; all, live,
  finished, upcoming &mdash; filtered without reloading the page.</p>
  <div class="onglets" id="onglets">{boutons}</div>
  <div id="liste">
    {''.join(bloc_match(m) for m in DONNEES['matchs'])}
  </div>
  <p class="rien" id="rien" hidden>No match in this state.</p>
</div></section>

<script>
(function () {{
  var boutons = document.querySelectorAll('#onglets .onglet');
  var matchs  = document.querySelectorAll('#liste .match');
  var rien    = document.getElementById('rien');
  function filtrer(cle) {{
    var vus = 0;
    matchs.forEach(function (m) {{
      var ok = (cle === 'all') || (m.dataset.etat === cle);
      m.hidden = !ok;
      if (ok) vus++;
    }});
    /* On le DIT quand il n'y a rien. Une liste vide sans phrase ressemble a
       une page cassee, et personne n'ouvre la console pour verifier. */
    rien.hidden = vus > 0;
    boutons.forEach(function (b) {{
      b.setAttribute('aria-pressed', String(b.dataset.f === cle));
    }});
  }}
  boutons.forEach(function (b) {{
    b.addEventListener('click', function () {{ filtrer(b.dataset.f); }});
  }});
}})();
</script>
"""


# ===========================================================================
# 3. JOUEURS (liste + classement buteurs)
def joueurs_liste():
    tries = sorted(DONNEES["joueurs"], key=lambda j: (-j["buts"], -j["passes"], j["nom"]))
    lignes = "".join(
        f'<tr><td class="pos">{i}</td>'
        f'<td><a href="player-{E(j["slug"])}.html" style="text-decoration:none">{E(j["nom"])}</a></td>'
        f'<td style="color:var(--gris)">{E(j["poste"])}</td>'
        f'<td style="color:var(--gris)">{E(j["club"])}</td>'
        f'<td class="n">{j["matchs"]}</td><td class="n">{j["buts"]}</td>'
        f'<td class="n">{j["passes"]}</td><td class="n">{j["xg"]:.2f}</td></tr>'
        for i, j in enumerate(tries[:60], start=1))
    return f"""
<section class="sec"><div class="wrap">
  <h1>Players</h1>
  <p class="chapeau">Sixty of the {len(DONNEES['joueurs'])} invented players in
  this mockup, by goals. Every profile page is generated, so any row opens a
  full player page.</p>
  <div class="enroule"><table class="tab">
    <thead><tr><th class="pos"></th><th>Player</th><th>Position</th><th>Club</th>
      <th class="n">Apps</th><th class="n">G</th><th class="n">A</th><th class="n">xG</th></tr></thead>
    <tbody>{lignes}</tbody>
  </table></div>
</div></section>
"""


# ===========================================================================
# 4. FICHE JOUEUR
def fiche_joueur(j):
    c = club_par_slug(j["club_slug"])
    stats = [("Apps", j["matchs"]), ("Minutes", j["minutes"]), ("Goals", j["buts"]),
             ("Assists", j["passes"]), ("Shots", j["tirs"]),
             ("On target", j["tirs_cadres"]), ("xG", f'{j["xg"]:.2f}'),
             ("xA", f'{j["xa"]:.2f}')]
    blocs = "".join(f'<div class="st"><div class="v">{v}</div><div class="l">{E(l)}</div></div>'
                    for l, v in stats)
    infos = [
        ("Position", E(j["poste"])), ("Club", f'<a href="club-{E(c["slug"])}.html">{E(c["nom"])}</a>'),
        ("Nationality", E(j["pays"])), ("Age", str(j["age"])),
        ("Height", f'{j["taille"]} cm'), ("Weight", f'{j["poids"]} kg'),
        ("Preferred foot", E(j["pied"])), ("Squad number", str(j["numero"])),
        ("Contract until", E(j["fin_contrat"])),
        ("Estimated value", f'&euro;{j["valeur"]}M'),
        ("Available", "Yes" if j["disponible"] else "No"),
        ("Wages", tbd()), ("Injury record", tbd()),
        ("Agent", tbd()), ("Career history", tbd()),
    ]
    lignes = "".join(f'<div class="paire"><dt>{l}</dt><dd>{v}</dd></div>' for l, v in infos)
    return f"""
<section class="sec"><div class="wrap">
  <div class="profil">
    <div>
      <div class="fiche">
        <div class="avatar" style="background:{c['couleur']}">{E(initiales(j['nom']))}</div>
        <p class="nom">{E(j['nom'])}</p>
        <p class="sous">{E(j['poste'])} &middot; {E(c['nom'])}</p>
        <dl style="margin:0">{lignes}</dl>
      </div>
    </div>
    <div>
      <div class="sec-h"><h2>Season statistics</h2></div>
      <div class="stats">{blocs}</div>

      <div class="sec-h" style="margin-top:30px"><h2>Career history</h2></div>
      <div class="carte"><p>{tbd()}<br>
      Season-by-season history comes from the same licensed feed as the
      statistics above. The layout is ready for it; the rows are not invented.</p></div>

      <div class="sec-h" style="margin-top:30px"><h2>Videos</h2></div>
      <div class="carte"><p>A player uploading <b>his own</b> footage is
      straightforward and needs no licence. Match highlights are broadcast
      rights and are a separate negotiation &mdash; {tbd()}</p></div>

      <div class="sec-h" style="margin-top:30px"><h2>Scout reports</h2></div>
      <div class="carte"><p>{tbd()}<br>
      Reports are written inside the platform by verified scouts, so this
      section fills itself once that role exists. It depends on no external
      provider.</p></div>
    </div>
  </div>
</div></section>
"""


# ===========================================================================
# 5. CLUBS
def clubs_liste():
    cartes = "".join(f"""<a class="carte" href="club-{E(c['slug'])}.html" style="text-decoration:none">
      <h3>{ecu(c['couleur'], c['nom'])}</h3>
      <p>{E(c['ville'])}, {E(c['pays'])}<br>{E(c['stade'])} &middot; {c['capacite']:,} seats</p>
    </a>""".replace(",", " ") for c in DONNEES["clubs"])
    return f"""
<section class="sec"><div class="wrap">
  <h1>Clubs</h1>
  <p class="chapeau">Ten invented clubs. None of them exists; the cities are
  real, the clubs are not.</p>
  <div class="grille g3">{cartes}</div>
</div></section>
"""


def fiche_club(c):
    effectif = [j for j in DONNEES["joueurs"] if j["club_slug"] == c["slug"]]
    groupes = ["Goalkeepers", "Defenders", "Midfielders", "Forwards"]
    blocs = ""
    for g in groupes:
        gens = [j for j in effectif if j["groupe"] == g]
        lignes = "".join(
            f'<tr><td class="pos">{j["numero"]}</td>'
            f'<td><a href="player-{E(j["slug"])}.html" style="text-decoration:none">{E(j["nom"])}</a></td>'
            f'<td style="color:var(--gris)">{E(j["poste"])}</td>'
            f'<td class="n">{j["age"]}</td><td class="n">{j["matchs"]}</td>'
            f'<td class="n">{j["buts"]}</td></tr>' for j in gens)
        blocs += f"""<div class="sec-h" style="margin-top:26px"><h2>{E(g)}</h2></div>
        <div class="enroule"><table class="tab">
          <thead><tr><th class="pos">#</th><th>Player</th><th>Position</th>
          <th class="n">Age</th><th class="n">Apps</th><th class="n">G</th></tr></thead>
          <tbody>{lignes}</tbody></table></div>"""

    ligne_cl = [l for l in DONNEES["classement"] if l["club_slug"] == c["slug"]]
    if ligne_cl:
        l = ligne_cl[0]
        table = (f'<div class="stats"><div class="st"><div class="v">{l["rang"]}</div>'
                 f'<div class="l">Position</div></div>'
                 f'<div class="st"><div class="v">{l["points"]}</div><div class="l">Points</div></div>'
                 f'<div class="st"><div class="v">{l["victoires"]}</div><div class="l">Won</div></div>'
                 f'<div class="st"><div class="v">{l["difference"]:+d}</div><div class="l">GD</div></div></div>')
    else:
        table = f'<div class="carte"><p>Not in the league shown in this mockup &mdash; {tbd()}</p></div>'

    infos = [("Country", E(c["pays"])), ("City", E(c["ville"])),
             ("Stadium", E(c["stade"])), ("Capacity", f'{c["capacite"]:,}'.replace(",", " ")),
             ("Founded", str(c["fonde"])), ("Head coach", tbd()),
             ("President", tbd()), ("Official website", tbd())]
    lignes_i = "".join(f'<div class="paire"><dt>{l}</dt><dd>{v}</dd></div>' for l, v in infos)

    return f"""
<section class="sec"><div class="wrap">
  <div class="profil">
    <div><div class="fiche">
      <div class="avatar" style="background:{c['couleur']}">{E(c['code'])}</div>
      <p class="nom">{E(c['nom'])}</p>
      <p class="sous">{E(c['ville'])}, {E(c['pays'])}</p>
      <dl style="margin:0">{lignes_i}</dl>
    </div></div>
    <div>
      <div class="sec-h"><h2>League position</h2>
        <a class="plus" href="standings.html">Full table &rarr;</a></div>
      {table}
      {blocs}
      <div class="sec-h" style="margin-top:30px"><h2>Recruitment needs</h2></div>
      <div class="carte"><p>What a club is looking for is entered <b>by the
      club</b> in its dashboard, so this is one of the few sections that needs
      no data provider at all. See <a href="recruitment.html">Recruitment</a>.</p></div>
    </div>
  </div>
</div></section>
"""


def classement_page():
    lignes = "".join(
        f'<tr><td class="pos">{l["rang"]}</td>'
        f'<td><a href="club-{E(l["club_slug"])}.html" style="text-decoration:none">'
        f'{ecu(couleur_club(l["club_slug"]), l["club"])}</a></td>'
        f'<td class="n">{l["joues"]}</td><td class="n">{l["victoires"]}</td>'
        f'<td class="n">{l["nuls"]}</td><td class="n">{l["defaites"]}</td>'
        f'<td class="n">{l["marques"]}</td><td class="n">{l["encaisses"]}</td>'
        f'<td class="n">{l["difference"]:+d}</td>'
        f'<td class="n"><b>{l["points"]}</b></td></tr>'
        for l in DONNEES["classement"])
    nom_ligue = [n for k, n, _ in COMPETITIONS if k == LIGUE][0]
    return f"""
<section class="sec"><div class="wrap">
  <h1>{E(nom_ligue)}</h1>
  <p class="chapeau">An invented league of invented clubs. The arithmetic is
  consistent &mdash; played equals won plus drawn plus lost, and points follow
  the results &mdash; because a table that does not add up is the first thing
  a football reader notices.</p>
  <div class="enroule"><table class="tab">
    <thead><tr><th class="pos">#</th><th>Club</th><th class="n">P</th>
      <th class="n">W</th><th class="n">D</th><th class="n">L</th>
      <th class="n">GF</th><th class="n">GA</th><th class="n">GD</th>
      <th class="n">Pts</th></tr></thead>
    <tbody>{lignes}</tbody>
  </table></div>
</div></section>
"""


# ===========================================================================
# 6. RECRUTEMENT — le coeur commercial du cahier des charges.
def recrutement():
    # Les donnees partent en JSON dans la page : le filtrage se fait chez le
    # visiteur, sans serveur. C'est une maquette — mais le comportement, lui,
    # est le vrai : quatorze criteres, combinables, resultat immediat.
    charge = [{
        "n": j["nom"], "s": j["slug"], "p": j["poste"], "pc": j["poste_code"],
        "c": j["club"], "cs": j["club_slug"], "co": club_par_slug(j["club_slug"])["couleur"],
        "na": j["pays"], "a": j["age"], "t": j["taille"], "f": j["pied"],
        "v": j["valeur"], "d": 1 if j["disponible"] else 0,
        "g": j["buts"], "m": j["matchs"], "fc": j["fin_contrat"],
    } for j in DONNEES["joueurs"]]

    opt_poste = "".join(f'<option value="{c}">{E(l)}</option>' for c, l, _ in POSTES)
    opt_pays = "".join(f'<option value="{E(p)}">{E(p)}</option>' for p in sorted(PAYS))
    opt_pied = "".join(f'<option value="{E(p)}">{E(p)}</option>' for p in PIEDS)
    opt_fin = "".join(f'<option value="{a}">{a}</option>' for a in ("2026", "2027", "2028", "2029"))

    offres = [
        ("Central defender wanted", "Northgate United", ["CB", "18&ndash;25", "&euro;2M budget",
                                                         "3-year contract", "&gt;1.85 m"]),
        ("Left winger, immediate start", "Atletico Marena", ["LW", "20&ndash;27",
                                                             "&euro;4M budget", "Left foot"]),
        ("Goalkeeper, loan", "AS Belmont", ["GK", "Under 23", "Loan", "Available now"]),
    ]
    cartes_offres = "".join(f"""<div class="offre">
      <h3>{t}</h3><div class="club">{E(c)}</div>
      <div class="crit">{''.join(f'<span>{x}</span>' for x in crit)}</div>
    </div>""" for t, c, crit in offres)

    return f"""
<section class="sec"><div class="wrap">
  <h1>Recruitment</h1>
  <p class="chapeau">The commercial core of the brief: clubs post what they are
  looking for, and search a player database against fourteen criteria. The
  filters below are real &mdash; they run on {len(charge)} invented players and
  respond as you change them.</p>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-h"><h2>Open positions</h2></div>
  <div class="grille g3">{cartes_offres}</div>
  <p style="color:var(--gris);font-size:13px;margin-top:12px">Three examples,
  written by hand to show the shape. In the product a club fills this in from
  its dashboard.</p>
</div></section>

<section class="sec" style="padding-top:14px"><div class="wrap">
  <div class="sec-h"><h2>Find players</h2></div>
  <div class="recrut">
    <form class="filtres" id="filtres" onsubmit="return false">
      <div class="champ"><label for="fPos">Position</label>
        <select id="fPos"><option value="">Any</option>{opt_poste}</select></div>
      <div class="champ"><label for="fNat">Nationality</label>
        <select id="fNat"><option value="">Any</option>{opt_pays}</select></div>
      <div class="champ"><label>Age</label><div class="deux">
        <input id="fAgeMin" type="number" min="15" max="40" placeholder="min">
        <input id="fAgeMax" type="number" min="15" max="40" placeholder="max"></div></div>
      <div class="champ"><label for="fFoot">Preferred foot</label>
        <select id="fFoot"><option value="">Any</option>{opt_pied}</select></div>
      <div class="champ"><label for="fH">Minimum height (cm)</label>
        <input id="fH" type="number" min="150" max="210" placeholder="any"></div>
      <div class="champ"><label for="fVal">Maximum value (&euro;M)</label>
        <input id="fVal" type="number" min="0" max="100" step="0.1" placeholder="any"></div>
      <div class="champ"><label for="fGoals">Minimum goals</label>
        <input id="fGoals" type="number" min="0" max="50" placeholder="any"></div>
      <div class="champ"><label for="fEnd">Contract ends</label>
        <select id="fEnd"><option value="">Any</option>{opt_fin}</select></div>
      <div class="champ"><label for="fDispo">Availability</label>
        <select id="fDispo"><option value="">Any</option>
          <option value="1">Available only</option></select></div>
      <div class="champ"><label for="fNom">Name contains</label>
        <input id="fNom" type="search" placeholder="any"></div>
      <button class="btn btn-b" type="button" id="raz" style="width:100%">Reset</button>
    </form>

    <div>
      <p class="compte" id="compte"></p>
      <div id="res"></div>
      <p class="rien" id="rien" hidden>No player matches these criteria.</p>
    </div>
  </div>
</div></section>

<script id="donnees" type="application/json">{json.dumps(charge, ensure_ascii=False)}</script>
<script>
(function () {{
  var JOUEURS = JSON.parse(document.getElementById('donnees').textContent);
  var res = document.getElementById('res');
  var compte = document.getElementById('compte');
  var rien = document.getElementById('rien');
  var MAX = 40;   /* on n'affiche pas 240 lignes : on DIT combien on en cache */

  function val(id) {{
    var e = document.getElementById(id);
    return e.value === '' ? null : e.value;
  }}
  function nombre(id) {{
    var v = val(id);
    return v === null ? null : parseFloat(v);
  }}

  function filtrer() {{
    var pos = val('fPos'), nat = val('fNat'), foot = val('fFoot'),
        fin = val('fEnd'), dispo = val('fDispo'),
        nom = (val('fNom') || '').toLowerCase(),
        aMin = nombre('fAgeMin'), aMax = nombre('fAgeMax'),
        h = nombre('fH'), vMax = nombre('fVal'), gMin = nombre('fGoals');

    var gardes = JOUEURS.filter(function (j) {{
      if (pos   && j.pc !== pos) return false;
      if (nat   && j.na !== nat) return false;
      if (foot  && j.f  !== foot) return false;
      if (fin   && j.fc !== fin) return false;
      if (dispo && j.d  !== 1) return false;
      if (aMin !== null && j.a < aMin) return false;
      if (aMax !== null && j.a > aMax) return false;
      if (h    !== null && j.t < h) return false;
      if (vMax !== null && j.v > vMax) return false;
      if (gMin !== null && j.g < gMin) return false;
      if (nom && j.n.toLowerCase().indexOf(nom) === -1) return false;
      return true;
    }});

    gardes.sort(function (a, b) {{ return b.g - a.g || a.n.localeCompare(b.n); }});

    res.innerHTML = gardes.slice(0, MAX).map(function (j) {{
      return '<a class="jr" href="player-' + j.s + '.html">' +
        '<span class="init" style="background:' + j.co + '">' +
          j.n.split(' ')[0][0] + j.n.split(' ').pop()[0] + '</span>' +
        '<span><b>' + j.n + '</b><br><span class="meta">' + j.p + ' &middot; ' +
          j.c + ' &middot; ' + j.a + ' &middot; ' + j.t + ' cm &middot; ' +
          j.g + ' goals &middot; &euro;' + j.v + 'M</span></span>' +
        (j.d ? '<span class="dispo">Available</span>' : '<span></span>') +
      '</a>';
    }}).join('');

    /* Le nombre CACHE est ecrit. Une liste tronquee en silence se lit comme
       une liste complete, et un club conclurait qu'il n'y a que 40 joueurs. */
    if (gardes.length > MAX) {{
      compte.textContent = gardes.length + ' players match — showing the first ' +
        MAX + ', ' + (gardes.length - MAX) + ' more not shown';
    }} else {{
      compte.textContent = gardes.length + ' player' + (gardes.length === 1 ? '' : 's') + ' match';
    }}
    rien.hidden = gardes.length > 0;
    compte.hidden = gardes.length === 0;
  }}

  document.getElementById('filtres').addEventListener('input', filtrer);
  document.getElementById('filtres').addEventListener('change', filtrer);
  document.getElementById('raz').addEventListener('click', function () {{
    document.getElementById('filtres').reset();
    filtrer();
  }});
  filtrer();
}})();
</script>
"""


# ===========================================================================
# 7. LA PAGE HONNETE
def page_donnees():
    return f"""
<section class="sec"><div class="wrap">
  <h1>About the data</h1>
  <p class="chapeau">This page exists because the difference between this
  mockup and a live platform is not the design work &mdash; it is the data,
  and the data is bought, not built.</p>

  <div class="sec-h"><h2>Nothing here is real</h2></div>
  <div class="carte"><p>Ten clubs, {len(DONNEES['joueurs'])} players, one
  league table, eight matches. All invented. The cities are real; the clubs
  playing in them are not. No figure on this site describes a real footballer,
  and no real person is named anywhere.</p></div>

  <div class="sec-h" style="margin-top:30px"><h2>What has to be licensed</h2></div>
  <div class="grille g2">
    <div class="carte"><h3>Live scores and statistics</h3>
      <p>Minute-by-minute scores, line-ups, shots, possession, xG. These come
      from a data provider under contract &mdash; Opta/Stats Perform,
      Sportradar, SportMonks, API-Football and others. It is a monthly cost
      and it scales with coverage and refresh rate.</p></div>
    <div class="carte"><h3>Transfers and market values</h3>
      <p>A transfer database is compiled and sold. Market values in particular
      are a proprietary product of whoever publishes them.</p></div>
    <div class="carte"><h3>Match video</h3>
      <p>Highlights are broadcast rights, sold territory by territory. A
      platform cannot host them by embedding them from elsewhere either. A
      player's own footage is a different matter entirely, and that part is
      buildable today.</p></div>
    <div class="carte"><h3>Club identity and kit</h3>
      <p>Badges, names and shirts are trademarks. Selling or customising club
      kit needs a licence from the club or its manufacturer.</p></div>
  </div>

  <div class="sec-h" style="margin-top:30px"><h2>Players are people</h2></div>
  <div class="carte"><p>Date of birth, wages, market value and above all
  <b>injuries</b> are personal data about identifiable individuals; injuries
  are health data under Article 9 of the GDPR, which needs a lawful basis
  beyond ordinary consent. The brief already hedges this at point 4 &mdash;
  &ldquo;if legally available&rdquo;. It is worth deciding before the database
  is designed, not after.</p></div>

  <div class="sec-h" style="margin-top:30px"><h2>What needs nobody's permission</h2></div>
  <div class="carte"><p>This is the good news, and it is why the mockup leads
  with recruitment. Everything a <b>club, player, agent or scout types in
  themselves</b> is yours: profiles, availability, job postings,
  applications, shortlists, scout reports, messaging, uploaded video,
  verification badges, subscriptions. That is the whole of sections 6, 7, 9,
  18, 19, 20, 21 and 22 of the brief &mdash; and it is the part the brief
  itself calls the commercial core.</p></div>

  <div class="sec-h" style="margin-top:30px"><h2>What I need from you</h2></div>
  <div class="carte"><p>One decision unlocks the rest: <b>which data provider,
  and at what coverage</b>. It sets the database, the update mechanism and the
  monthly cost, and every module in sections 3, 4, 5, 11, 12 and 24 waits on
  it. Until then the recruitment side can be built in full &mdash; it depends
  on no one.</p></div>
</div></section>
"""


# ===========================================================================
if __name__ == "__main__":
    with open(os.path.join(RACINE, "assets", "site.css"), encoding="utf-8") as f:
        css = f.read()
    # Un commentaire CSS mal ferme tue en silence toutes les regles suivantes.
    assert css.count("/*") == css.count("*/"), \
        "assets/site.css : commentaires desequilibres"

    print(f"{MARQUE} — maquette")
    page("index.html", f"{MARQUE} — {BASELINE}",
         "A working mockup of a football platform: live scores, player and club "
         "profiles, and a recruitment marketplace. All data invented.", accueil())
    page("live.html", f"Live scores — {MARQUE}",
         "Matches by state: live, finished, upcoming.", scores())
    page("players.html", f"Players — {MARQUE}",
         "Player rankings and profiles in the mockup.", joueurs_liste())
    page("clubs.html", f"Clubs — {MARQUE}",
         "The ten invented clubs of the mockup.", clubs_liste())
    page("standings.html", f"Standings — {MARQUE}",
         "The league table of the mockup.", classement_page(), actuel="clubs.html")
    page("recruitment.html", f"Recruitment — {MARQUE}",
         "Club job postings and a player search with fourteen working filters.",
         recrutement())
    page("data.html", f"About the data — {MARQUE}",
         "What is invented here, what has to be licensed, and what needs "
         "nobody's permission.", page_donnees())

    for c in DONNEES["clubs"]:
        page(f"club-{c['slug']}.html", f"{c['nom']} — {MARQUE}",
             f"Club profile for {c['nom']} in the mockup.", fiche_club(c),
             actuel="clubs.html")
    for j in DONNEES["joueurs"]:
        page(f"player-{j['slug']}.html", f"{j['nom']} — {MARQUE}",
             f"Player profile for {j['nom']} in the mockup.", fiche_joueur(j),
             actuel="players.html")

    print("termine —", RACINE)
