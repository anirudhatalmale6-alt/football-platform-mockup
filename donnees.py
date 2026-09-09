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
CLUBS = [
    ("Northgate United", "NGU", "England", "Manchester", "Northgate Park", 41200, "#1F4E8C"),
    ("Riverfell FC", "RVF", "England", "Leeds", "Riverfell Ground", 28400, "#8C1F2F"),
    ("Atletico Marena", "AMA", "Spain", "Valencia", "Estadio Marena", 36800, "#C8551F"),
    ("Real Costanera", "RCO", "Spain", "Malaga", "Campo Costanera", 24100, "#1F7A5A"),
    ("Olympique Vaudreuil", "OVA", "France", "Lille", "Stade Vaudreuil", 33500, "#2F3E8C"),
    ("AS Belmont", "ASB", "France", "Nantes", "Parc Belmont", 21700, "#5A1F7A"),
    ("Werder Falkenau", "WFA", "Germany", "Dortmund", "Falkenau Arena", 45300, "#1F6B8C"),
    ("SV Hollenstein", "SVH", "Germany", "Bremen", "Hollenstein Stadion", 19800, "#7A5A1F"),
    ("Milano Verdi", "MIV", "Italy", "Turin", "Stadio Verdi", 30900, "#1F8C4E"),
    ("Sporting Aveiro Nova", "SAN", "Portugal", "Aveiro", "Estadio Nova", 17600, "#8C1F6B"),
]

PRENOMS = ["Adam", "Luca", "Yassine", "Diego", "Noah", "Kofi", "Emre", "Tobias",
           "Mateo", "Iker", "Samuel", "Rafael", "Jonas", "Hugo", "Amadou",
           "Viktor", "Ilias", "Marcus", "Andres", "Kenji", "Oskar", "Malik",
           "Tomas", "Bruno", "Elias", "Nico", "Ravi", "Sory", "Pedro", "Leon"]

NOMS = ["Brandt", "Okafor", "Ferreira", "Nowak", "Haddad", "Lindqvist",
        "Mensah", "Vasquez", "Delacroix", "Karlsen", "Bouchard", "Reyes",
        "Sundberg", "Adeyemi", "Moreno", "Vidal", "Kaneko", "Petrov",
        "Salgado", "Novak", "Traore", "Rossi", "Duarte", "Halvorsen",
        "Zerrouki", "Baptiste", "Meyer", "Costa", "Lindberg", "Abara"]

COMPETITIONS = [
    ("continental-cup", "Continental Cup", "Europe"),
    ("northern-league", "Northern League", "England"),
    ("liga-meridional", "Liga Meridional", "Spain"),
    ("championnat-national", "Championnat National", "France"),
    ("bundesliga-nord", "Bundesliga Nord", "Germany"),
]

# La ligue dont la maquette montre le classement complet.
LIGUE = "northern-league"


def _slug(texte):
    return "".join(c.lower() if c.isalnum() else "-" for c in texte).strip("-") \
        .replace("--", "-").replace("--", "-")


def construire():
    """Fabrique le jeu de donnees complet, deterministe."""
    rnd = random.Random(GRAINE)

    clubs = []
    for i, (nom, code, pays, ville, stade, capacite, couleur) in enumerate(CLUBS):
        clubs.append({
            "id": i + 1,
            "slug": _slug(nom),
            "nom": nom,
            "code": code,
            "pays": pays,
            "ville": ville,
            "stade": stade,
            "capacite": capacite,
            "couleur": couleur,
            "fonde": rnd.randint(1899, 1974),
            # Ce que la maquette NE PEUT PAS inventer sans mentir sur une
            # personne : le nom de l'entraineur et celui du president.
            "entraineur": VIDE,
            "president": VIDE,
            "site": VIDE,
        })

    joueurs = []
    identifiant = 0
    for club in clubs:
        # Un effectif credible : 3 gardiens, 7 defenseurs, 7 milieux, 5 attaquants.
        plan = ([POSTES[0]] * 3 + [POSTES[1]] * 3 + [POSTES[2]] * 2 + [POSTES[3]] * 2
                + [POSTES[4]] * 2 + [POSTES[5]] * 3 + [POSTES[6]] * 2
                + [POSTES[7]] * 2 + [POSTES[8]] * 2 + [POSTES[9]] * 3)
        for numero, (code_poste, poste, groupe) in enumerate(plan, start=1):
            identifiant += 1
            age = rnd.randint(17, 34)
            taille = rnd.randint(168, 197) if code_poste != "GK" else rnd.randint(185, 199)
            poids = int(taille * rnd.uniform(0.40, 0.46))

            matchs = rnd.randint(4, 34)
            # Les minutes NE PEUVENT PAS depasser matchs x 90.
            minutes = rnd.randint(matchs * 25, matchs * 90)

            if code_poste == "GK":
                tirs = 0
                tirs_cadres = 0
                buts = 0
                passes_d = rnd.randint(0, 1)
            else:
                pointe = {"ST": 2.6, "LW": 1.9, "RW": 1.9, "AM": 1.6}.get(code_poste, 0.7)
                tirs = int(rnd.uniform(0.3, 1.4) * pointe * matchs)
                # Cadres <= tirs, buts <= cadres. L'ordre est ce qui rend la
                # ligne lisible ; l'inverse saute aux yeux d'un lecteur foot.
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
                # La disponibilite est une donnee DECLAREE par le joueur ou son
                # agent, pas une donnee de fournisseur : elle peut exister sans
                # licence. C'est d'ailleurs la seule brique du recrutement qui
                # n'attend rien de personne.
                "disponible": rnd.choices([True, False], weights=[35, 65])[0],
                "salaire": VIDE,
                "blessures": VIDE,
            })

    # Classement : coherent (joues = V+N+D, points = 3V+N).
    classement = []
    for club in clubs[:8]:
        joues = 24
        victoires = rnd.randint(4, 17)
        nuls = rnd.randint(0, joues - victoires)
        defaites = joues - victoires - nuls
        marques = rnd.randint(victoires, victoires * 3 + 8)
        encaisses = rnd.randint(defaites, defaites * 3 + 8)
        classement.append({
            "club": club["nom"], "club_slug": club["slug"], "code": club["code"],
            "joues": joues, "victoires": victoires, "nuls": nuls,
            "defaites": defaites, "marques": marques, "encaisses": encaisses,
            "difference": marques - encaisses,
            "points": victoires * 3 + nuls,
        })
    classement.sort(key=lambda l: (-l["points"], -l["difference"], -l["marques"]))
    for rang, ligne in enumerate(classement, start=1):
        ligne["rang"] = rang

    # Matchs : trois etats, parce que c'est la navigation demandee au point 3
    # (En direct / Termines / A venir).
    matchs = []
    paires = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (1, 2), (3, 4), (5, 6)]
    etats = ["live", "live", "termine", "termine", "termine", "avenir",
             "avenir", "avenir"]
    for i, ((a, b), etat) in enumerate(zip(paires, etats)):
        dom, ext = clubs[a], clubs[b]
        m = {
            "id": i + 1,
            "domicile": dom["nom"], "domicile_slug": dom["slug"], "domicile_code": dom["code"],
            "exterieur": ext["nom"], "exterieur_slug": ext["slug"], "exterieur_code": ext["code"],
            "competition": rnd.choice(COMPETITIONS)[1],
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

    return {"clubs": clubs, "joueurs": joueurs, "classement": classement,
            "matchs": matchs}


DONNEES = construire()

# ---------------------------------------------------------------------------
# Controles de coherence. Ils tournent A LA GENERATION : un jeu de donnees
# impossible ne doit jamais atteindre une capture d'ecran.
for _j in DONNEES["joueurs"]:
    assert _j["minutes"] <= _j["matchs"] * 90, f"{_j['nom']} : plus de minutes que de matchs"
    assert _j["tirs_cadres"] <= _j["tirs"], f"{_j['nom']} : plus de tirs cadres que de tirs"
    assert _j["buts"] <= _j["tirs_cadres"], f"{_j['nom']} : plus de buts que de tirs cadres"
for _l in DONNEES["classement"]:
    assert _l["victoires"] + _l["nuls"] + _l["defaites"] == _l["joues"], \
        f"{_l['club']} : le total des resultats ne fait pas le nombre de matchs joues"
    assert _l["points"] == _l["victoires"] * 3 + _l["nuls"], \
        f"{_l['club']} : les points ne suivent pas les resultats"
