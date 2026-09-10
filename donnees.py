# -*- coding: utf-8 -*-
"""
Les donnees de la maquette « Football All-in-One ».

TOUT CE FICHIER EST FICTIF, ET C'EST UN CHOIX, PAS UN MANQUE DE TEMPS.

Trois raisons, dans l'ordre de ce qu'elles coutent :

1. LES DONNEES REELLES SE LOUENT. Scores en direct, statistiques, xG, valeurs
   de marche, transferts : personne ne les produit soi-meme. Elles viennent
   d'un fournisseur sous licence (Opta/Stats Perform, Sportradar, SportMonks,
   API-Football...), avec un contrat et un abonnement mensuel. Le cahier des
   charges le dit lui-meme au point 24 : « il faudra verifier les droits ».
   Tant que ce contrat n'existe pas, aucune donnee reelle ne peut figurer ici.

2. UN JOUEUR EST UNE PERSONNE. Nom, date de naissance, salaire, valeur de
   marche, et surtout les BLESSURES — le RGPD en fait des donnees de sante,
   article 9. Publier ca sans base legale n'est pas un detail technique.

3. LES CLUBS ET LES COMPETITIONS SONT DES MARQUES. Logos, noms, maillots.

Donc : clubs inventes, joueurs inventes, chiffres inventes, et CHAQUE PAGE LE
DIT A L'ECRAN. La maquette montre la FORME du produit — ce qu'on voit, ce sur
quoi on clique, comment on filtre — pas des faits sur le football reel.

Les chiffres sont tout de meme COHERENTS entre eux (un joueur ne marque pas
plus de buts qu'il n'a de tirs cadres, ne joue pas plus de minutes qu'il n'a
de matchs x 90). Une maquette aux chiffres impossibles ne se lit pas : l'oeil
s'arrete sur l'absurdite au lieu de juger l'interface.
"""
import random

# Le vocabulaire du vide POUR CE PRODUIT, et pour lui seul. Chaque produit du
# client a le sien ; les melanger rend le mot invisible.
VIDE = "To be sourced"

MARQUE = "Football All-in-One"
BASELINE = "Everything in one place"

# Une graine fixe : le meme dataset a chaque generation. Sans elle, deux
# captures d'ecran prises a dix minutes d'intervalle montreraient des chiffres
# differents, et le client croirait a un bug.
GRAINE = 20260909

POSTES = [
    ("GK", "Goalkeeper", "Goalkeepers"),
    ("CB", "Centre-back", "Defenders"),
    ("LB", "Left-back", "Defenders"),
    ("RB", "Right-back", "Defenders"),
    ("DM", "Defensive midfielder", "Midfielders"),
    ("CM", "Central midfielder", "Midfielders"),
    ("AM", "Attacking midfielder", "Midfielders"),
    ("LW", "Left winger", "Forwards"),
    ("RW", "Right winger", "Forwards"),
    ("ST", "Striker", "Forwards"),
]

PIEDS = ["Right", "Left", "Both"]

# Pays reels : ce sont des nationalites, pas des affirmations sur quelqu'un.
# Aucun d'eux n'est associe a une personne reelle dans ce fichier.
PAYS = ["France", "Brazil", "Nigeria", "Morocco", "Spain", "Argentina",
        "Senegal", "Portugal", "Japan", "Norway", "Croatia", "Ghana",
        "Colombia", "Netherlands", "Egypt", "Sweden"]

# Clubs INVENTES. Aucun ne correspond a un club existant ; les villes sont
# reelles mais aucun de ces clubs n'y joue.
# LES LIGUES, ET LES CLUBS DEDANS.
#
# Le client a demande l'ordre explicitement : « il faut les ligues, ensuite les
# clubs ». Ce n'est pas qu'une question de menu — c'est la structure du sport.
# Un club n'existe pas tout seul : il joue dans une division, et c'est la
# division qui produit le classement, le calendrier et le sens du mot
# « premier ». L'ancienne version avait dix clubs eparpilles dans six pays et
# UN classement arbitraire : on ne pouvait pas repondre a « qui mene en
# Espagne », parce que la question n'avait pas de support.
#
# Quatre championnats de huit clubs, plus une coupe continentale qui n'a PAS de
# classement (une coupe se joue en elimination directe, et afficher un tableau
# la-dedans serait faux).
LIGUES = [
    ("northern-league",      "Northern League",      "England", "#1F4E8C"),
    ("liga-meridional",      "Liga Meridional",      "Spain",   "#C8551F"),
    ("championnat-national", "Championnat National", "France",  "#2F3E8C"),
    ("bundesliga-nord",      "Bundesliga Nord",      "Germany", "#1F6B8C"),
]

COUPE = ("continental-cup", "Continental Cup", "Europe")

# Huit clubs par championnat. Tous INVENTES. Les villes sont reelles, les clubs
# qui y jouent ne le sont pas — et aucun nom ne reprend celui d'un club
# existant, ce que la suite de controles verifie sur une liste de vrais noms.
CLUBS_PAR_LIGUE = {
    "northern-league": [
        ("Northgate United",    "NGU", "Manchester", "Northgate Park",     41200, "#1F4E8C"),
        ("Riverfell FC",        "RVF", "Leeds",      "Riverfell Ground",   28400, "#8C1F2F"),
        ("Ashford Town",        "ASH", "Sheffield",  "Ashford Lane",       22600, "#3E6B2F"),
        ("Kingsmoor City",      "KMC", "Bristol",    "Kingsmoor Stadium",  34900, "#5A2F8C"),
        ("Weyburn Rovers",      "WEY", "Newcastle",  "Weyburn Road",       26100, "#1F7A5A"),
        ("Thorncliff Athletic", "THA", "Nottingham", "Thorncliff Park",    19800, "#8C6B1F"),
        ("Barrowdale FC",       "BAR", "Hull",       "Barrowdale Ground",  17400, "#2F5A8C"),
        ("Elmsworth United",    "ELM", "Coventry",   "Elmsworth Stadium",  24300, "#7A2F4E"),
    ],
    "liga-meridional": [
        ("Atletico Marena",     "AMA", "Valencia",   "Estadio Marena",     36800, "#C8551F"),
        ("Real Costanera",      "RCO", "Malaga",     "Campo Costanera",    24100, "#1F7A5A"),
        ("CD Valcorta",         "VAL", "Zaragoza",   "Estadio Valcorta",   28700, "#8C1F2F"),
        ("Union Mirasol",       "MIR", "Murcia",     "Campo Mirasol",      18900, "#B4690E"),
        ("Racing Valmareda",    "RVA", "Vigo",       "Estadio Valmareda",  31200, "#1F4E8C"),
        ("CF Altamira",         "ALT", "Cordoba",    "Campo Altamira",     21500, "#5A2F8C"),
        ("Deportivo Sierrablanca", "SIE", "Granada", "Estadio Sierrablanca", 26400, "#2F6B4E"),
        ("Atletico Roldana",    "ROL", "Alicante",   "Campo Roldana",      16800, "#7A4E1F"),
    ],
    "championnat-national": [
        ("Olympique Vaudreuil", "OVA", "Lille",      "Stade Vaudreuil",    33500, "#2F3E8C"),
        ("AS Belmont",          "ASB", "Nantes",     "Parc Belmont",       21700, "#5A1F7A"),
        ("FC Vireval",          "VIR", "Toulouse",   "Stade Vireval",      27300, "#8C2F1F"),
        ("Racing Montclair",    "MTC", "Strasbourg", "Stade Montclair",    24800, "#1F6B4E"),
        ("US Beauport",         "BEA", "Rennes",     "Parc Beauport",      19600, "#4E1F8C"),
        ("Stade Ferrand",       "FER", "Reims",      "Stade Ferrand",      17900, "#8C6B1F"),
        ("AC Rochemont",        "ROC", "Montpellier", "Parc Rochemont",    29100, "#1F5A8C"),
        ("FC Saint-Aubin",      "STA", "Angers",     "Stade Saint-Aubin",  15400, "#6B2F5A"),
    ],
    "bundesliga-nord": [
        ("FC Falkenau",         "FAL", "Dortmund",   "Falkenau Arena",     45300, "#1F6B8C"),
        ("SV Hollenstein",      "SVH", "Bremen",     "Hollenstein Stadion", 19800, "#7A5A1F"),
        ("FC Rotenbach",        "ROT", "Hannover",   "Rotenbach Arena",    32700, "#8C1F4E"),
        ("TSV Grunbach",        "GRU", "Nuremberg",  "Grunbach Stadion",   23900, "#2F7A3E"),
        ("SC Adlerhorst",       "ADL", "Duisburg",   "Adlerhorst Arena",   28200, "#1F3E8C"),
        ("VfB Steinfeld",       "STE", "Augsburg",   "Steinfeld Stadion",  20600, "#8C5A1F"),
        ("FC Wildenau",         "WIL", "Bochum",     "Wildenau Arena",     26800, "#5A1F8C"),
        ("SV Lindhorst",        "LIN", "Kiel",       "Lindhorst Stadion",  16200, "#1F7A6B"),
    ],
}

# Conserve pour le reste du code : la liste plate de toutes les competitions.
COMPETITIONS = [(COUPE[0], COUPE[1], COUPE[2])] + \
               [(k, n, p) for k, n, p, _ in LIGUES]

PRENOMS = ["Adam", "Luca", "Yassine", "Diego", "Noah", "Kofi", "Emre", "Tobias",
           "Mateo", "Iker", "Samuel", "Rafael", "Jonas", "Hugo", "Amadou",
           "Viktor", "Ilias", "Marcus", "Andres", "Kenji", "Oskar", "Malik",
           "Tomas", "Bruno", "Elias", "Nico", "Ravi", "Sory", "Pedro", "Leon"]

NOMS = ["Brandt", "Okafor", "Ferreira", "Nowak", "Haddad", "Lindqvist",
        "Mensah", "Vasquez", "Delacroix", "Karlsen", "Bouchard", "Reyes",
        "Sundberg", "Adeyemi", "Moreno", "Vidal", "Kaneko", "Petrov",
        "Salgado", "Novak", "Traore", "Rossi", "Duarte", "Halvorsen",
        "Zerrouki", "Baptiste", "Meyer", "Costa", "Lindberg", "Abara"]



def _slug(texte):
    return "".join(c.lower() if c.isalnum() else "-" for c in texte).strip("-") \
        .replace("--", "-").replace("--", "-")


def construire():
    """Fabrique le jeu de donnees complet, deterministe.

    L'ordre suit celui du sport, et celui que le client a demande : d'abord les
    LIGUES, puis les CLUBS qui les composent, puis les joueurs de ces clubs,
    puis les classements qui decoulent des clubs, puis les matchs.
    """
    rnd = random.Random(GRAINE)

    # --- 1. les ligues, et les clubs dedans ------------------------------
    ligues = []
    clubs = []
    identifiant_club = 0
    for cle, nom_ligue, pays_ligue, couleur_ligue in LIGUES:
        membres = []
        for nom, code, ville, stade, capacite, couleur in CLUBS_PAR_LIGUE[cle]:
            identifiant_club += 1
            club = {
                "id": identifiant_club,
                "slug": _slug(nom),
                "nom": nom,
                "code": code,
                "pays": pays_ligue,
                "ville": ville,
                "stade": stade,
                "capacite": capacite,
                "couleur": couleur,
                "ligue": cle,
                "ligue_nom": nom_ligue,
                "fonde": rnd.randint(1899, 1974),
                # Ce que la maquette NE PEUT PAS inventer sans mentir sur une
                # personne reelle : l'entraineur et le president.
                "entraineur": VIDE,
                "president": VIDE,
                "site": VIDE,
            }
            clubs.append(club)
            membres.append(club["slug"])
        ligues.append({
            "cle": cle, "nom": nom_ligue, "pays": pays_ligue,
            "couleur": couleur_ligue, "clubs": membres,
            "type": "championnat",
        })

    # La coupe : PAS de classement. Une coupe se joue en elimination directe,
    # et publier un tableau la-dedans serait une erreur de fond, pas
    # d'affichage.
    ligues.append({
        "cle": COUPE[0], "nom": COUPE[1], "pays": COUPE[2],
        "couleur": "#7A5A1F",
        "clubs": [c["slug"] for c in clubs if rnd.random() < 0.35],
        "type": "coupe",
    })

    # --- 2. les joueurs ---------------------------------------------------
    joueurs = []
    identifiant = 0
    for club in clubs:
        # Un effectif credible et lisible : 2 gardiens, 6 defenseurs,
        # 6 milieux, 4 attaquants.
        plan = ([POSTES[0]] * 2 + [POSTES[1]] * 2 + [POSTES[2]] + [POSTES[3]]
                + [POSTES[4]] * 2 + [POSTES[5]] * 2 + [POSTES[6]] * 2
                + [POSTES[7]] + [POSTES[8]] + [POSTES[9]] * 2)
        for numero, (code_poste, poste, groupe) in enumerate(plan, start=1):
            identifiant += 1
            age = rnd.randint(17, 34)
            taille = rnd.randint(168, 197) if code_poste != "GK" else rnd.randint(185, 199)
            poids = int(taille * rnd.uniform(0.40, 0.46))

            matchs = rnd.randint(4, 34)
            minutes = rnd.randint(matchs * 25, matchs * 90)

            if code_poste == "GK":
                tirs = tirs_cadres = buts = 0
                passes_d = rnd.randint(0, 1)
            else:
                pointe = {"ST": 2.6, "LW": 1.9, "RW": 1.9, "AM": 1.6}.get(code_poste, 0.7)
                tirs = int(rnd.uniform(0.3, 1.4) * pointe * matchs)
                tirs_cadres = int(tirs * rnd.uniform(0.30, 0.55))
                buts = int(tirs_cadres * rnd.uniform(0.15, 0.45))
                passes_d = rnd.randint(0, max(1, int(matchs * 0.3)))

            valeur = rnd.choice([0.3, 0.6, 1.2, 2.5, 4.0, 6.5, 9.0, 14.0, 22.0, 35.0])
            if age > 30:
                valeur = round(valeur * 0.55, 1)
            if age < 21 and buts > 6:
                valeur = round(valeur * 1.6, 1)

            joueurs.append({
                "id": identifiant,
                "slug": f"player-{identifiant}",
                "nom": f"{rnd.choice(PRENOMS)} {rnd.choice(NOMS)}",
                "numero": numero,
                "poste": poste,
                "poste_code": code_poste,
                "groupe": groupe,
                "club": club["nom"],
                "club_slug": club["slug"],
                "ligue": club["ligue"],
                "ligue_nom": club["ligue_nom"],
                "pays": rnd.choice(PAYS),
                "age": age,
                "taille": taille,
                "poids": poids,
                "pied": rnd.choice(PIEDS),
                "matchs": matchs,
                "minutes": minutes,
                "buts": buts,
                "passes": passes_d,
                "tirs": tirs,
                "tirs_cadres": tirs_cadres,
                "jaunes": rnd.randint(0, 9),
                "rouges": rnd.choices([0, 1], weights=[92, 8])[0],
                "xg": round(buts * rnd.uniform(0.75, 1.35), 2),
                "xa": round(passes_d * rnd.uniform(0.70, 1.40), 2),
                "valeur": valeur,
                "fin_contrat": rnd.choice(["2026", "2027", "2028", "2029"]),
                "disponible": rnd.choices([True, False], weights=[35, 65])[0],
                "salaire": VIDE,
                "blessures": VIDE,
            })

    # --- 3. UN CLASSEMENT PAR CHAMPIONNAT, SIMULE ------------------------
    # Le classement n'est PAS tire au sort ligne par ligne : la saison est
    # JOUEE, en aller-retour, et le tableau est la somme des resultats.
    #
    # C'est la seule facon d'obtenir un tableau possible. Un tirage par ligne
    # donne des colonnes qui s'additionnent chacune correctement et une ligue
    # qui ne peut pas exister : les victoires du championnat ne valent plus ses
    # defaites, les buts marques ne valent plus les buts encaisses, et huit
    # clubs affichent 24 journees quand un aller-retour a huit n'en produit
    # que 14. Un lecteur de football voit ca tout de suite, et il cesse de
    # regarder le reste.
    classements = {}
    for ligue in ligues:
        if ligue["type"] != "championnat":
            continue
        membres = ligue["clubs"]
        stat = {s: {"joues": 0, "victoires": 0, "nuls": 0, "defaites": 0,
                    "marques": 0, "encaisses": 0} for s in membres}
        for i, dom in enumerate(membres):
            for j, ext in enumerate(membres):
                if i == j:
                    continue
                # Aller-retour : chaque paire se rencontre deux fois, une fois
                # chez chacun.
                bd = rnd.choices([0, 1, 2, 3, 4, 5], weights=[16, 26, 24, 18, 10, 6])[0]
                be = rnd.choices([0, 1, 2, 3, 4], weights=[22, 28, 24, 16, 10])[0]
                stat[dom]["joues"] += 1
                stat[ext]["joues"] += 1
                stat[dom]["marques"] += bd
                stat[dom]["encaisses"] += be
                stat[ext]["marques"] += be
                stat[ext]["encaisses"] += bd
                if bd > be:
                    stat[dom]["victoires"] += 1
                    stat[ext]["defaites"] += 1
                elif bd < be:
                    stat[ext]["victoires"] += 1
                    stat[dom]["defaites"] += 1
                else:
                    stat[dom]["nuls"] += 1
                    stat[ext]["nuls"] += 1

        table = []
        for slug in membres:
            club = [c for c in clubs if c["slug"] == slug][0]
            st = stat[slug]
            table.append({
                "club": club["nom"], "club_slug": slug, "code": club["code"],
                "joues": st["joues"], "victoires": st["victoires"],
                "nuls": st["nuls"], "defaites": st["defaites"],
                "marques": st["marques"], "encaisses": st["encaisses"],
                "difference": st["marques"] - st["encaisses"],
                "points": st["victoires"] * 3 + st["nuls"],
            })
        table.sort(key=lambda l: (-l["points"], -l["difference"], -l["marques"]))
        for rang, ligne in enumerate(table, start=1):
            ligne["rang"] = rang
        classements[ligue["cle"]] = table

    # --- 4. les matchs, rattaches a leur competition ----------------------
    matchs = []
    identifiant_match = 0
    for ligue in ligues:
        membres = ligue["clubs"]
        if len(membres) < 2:
            continue
        # Trois etats par competition : c'est la navigation demandee au point 3
        # du cahier des charges (En direct / Termines / A venir).
        for decalage, etat in ((0, "live"), (2, "termine"), (4, "avenir")):
            if decalage + 1 >= len(membres):
                continue
            identifiant_match += 1
            dom = [c for c in clubs if c["slug"] == membres[decalage]][0]
            ext = [c for c in clubs if c["slug"] == membres[decalage + 1]][0]
            m = {
                "id": identifiant_match,
                "domicile": dom["nom"], "domicile_slug": dom["slug"],
                "domicile_code": dom["code"],
                "exterieur": ext["nom"], "exterieur_slug": ext["slug"],
                "exterieur_code": ext["code"],
                "competition": ligue["nom"],
                "competition_cle": ligue["cle"],
                "etat": etat,
                "heure": f"{rnd.randint(13, 20)}:{rnd.choice(['00', '15', '30', '45'])}",
            }
            if etat == "avenir":
                m.update({"score_dom": None, "score_ext": None, "minute": None})
            else:
                m["score_dom"] = rnd.randint(0, 4)
                m["score_ext"] = rnd.randint(0, 3)
                m["minute"] = rnd.randint(12, 88) if etat == "live" else 90
            matchs.append(m)

    return {"clubs": clubs, "joueurs": joueurs, "ligues": ligues,
            "classements": classements, "matchs": matchs}


DONNEES = construire()

# ---------------------------------------------------------------------------
# Controles de coherence. Ils tournent A LA GENERATION : un jeu de donnees
# impossible ne doit jamais atteindre une capture d'ecran.
for _j in DONNEES["joueurs"]:
    assert _j["minutes"] <= _j["matchs"] * 90, f"{_j['nom']} : plus de minutes que de matchs"
    assert _j["tirs_cadres"] <= _j["tirs"], f"{_j['nom']} : plus de tirs cadres que de tirs"
    assert _j["buts"] <= _j["tirs_cadres"], f"{_j['nom']} : plus de buts que de tirs cadres"
for _cle, _table in DONNEES["classements"].items():
    for _l in _table:
        assert _l["victoires"] + _l["nuls"] + _l["defaites"] == _l["joues"], \
            f"{_l['club']} : le total des resultats ne fait pas le nombre de matchs joues"
        assert _l["points"] == _l["victoires"] * 3 + _l["nuls"], \
            f"{_l['club']} : les points ne suivent pas les resultats"
        assert _l["difference"] == _l["marques"] - _l["encaisses"], \
            f"{_l['club']} : la difference de buts ne suit pas les buts"
    # ET AU NIVEAU DE LA LIGUE. Une ligue ou les victoires ne valent pas les
    # defaites, ou dont les buts marques ne valent pas les buts encaisses, ne
    # peut pas avoir ete jouee — meme si chaque ligne s'additionne.
    assert sum(_l["victoires"] for _l in _table) == sum(_l["defaites"] for _l in _table), \
        f"{_cle} : autant de victoires que de defaites, sinon la saison est impossible"
    assert sum(_l["nuls"] for _l in _table) % 2 == 0, \
        f"{_cle} : un nul se compte pour deux clubs, le total doit etre pair"
    assert sum(_l["marques"] for _l in _table) == sum(_l["encaisses"] for _l in _table), \
        f"{_cle} : chaque but marque est encaisse par quelqu'un"
    _n = len(_table)
    for _l in _table:
        assert _l["joues"] == 2 * (_n - 1), \
            f"{_l['club']} : {_l['joues']} journees pour un aller-retour a {_n} clubs"

# Un club appartient a UN championnat et un seul. Sans cette regle, un club
# apparaitrait dans deux classements et la question « qui est premier » aurait
# deux reponses.
_vus = {}
for _lg in DONNEES["ligues"]:
    if _lg["type"] != "championnat":
        continue
    for _slug in _lg["clubs"]:
        assert _slug not in _vus, f"{_slug} : dans deux championnats ({_vus.get(_slug)} et {_lg['cle']})"
        _vus[_slug] = _lg["cle"]
assert len(_vus) == len(DONNEES["clubs"]), \
    f"{len(DONNEES['clubs']) - len(_vus)} club(s) sans championnat"

# Chaque classement compte exactement les clubs de sa ligue.
for _lg in DONNEES["ligues"]:
    if _lg["type"] != "championnat":
        continue
    assert len(DONNEES["classements"][_lg["cle"]]) == len(_lg["clubs"]), \
        f"{_lg['cle']} : classement de {len(DONNEES['classements'][_lg['cle']])} lignes " \
        f"pour {len(_lg['clubs'])} clubs"

# La coupe n'a PAS de classement, et c'est volontaire.
assert COUPE[0] not in DONNEES["classements"], \
    "la coupe ne doit pas avoir de classement : elle se joue en elimination directe"
