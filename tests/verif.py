# -*- coding: utf-8 -*-
"""
Controles de la maquette Football All-in-One, AU RENDU.

Ce qui compte ici n'est pas « la page s'affiche » mais :
  1. le filtre de recrutement rend EXACTEMENT l'ensemble qu'un recalcul
     independant, fait depuis donnees.py, designe — c'est le coeur commercial
     du cahier des charges, et un filtre qui se trompe en silence vend un
     joueur qui ne correspond pas ;
  2. aucune personne ni aucun club REEL n'est nomme nulle part ;
  3. chaque page dit qu'elle est une maquette.

Usage : python3 tests/verif.py http://127.0.0.1:8921
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright

from donnees import COUPE, DONNEES, VIDE

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8921").rstrip("/")

PAGES = ["index.html", "live.html", "players.html", "clubs.html",
         "competitions.html", "league-northern-league.html",
         "recruitment.html", "data.html",
         "club-northgate-united.html", "player-player-1.html"]

# Controle negatif : des noms REELS qui ne doivent apparaitre nulle part. Le
# cahier des charges en citait (Mbappe, Real Madrid) ; les reprendre aurait
# publie des donnees personnelles inventees sur des gens qui existent.
REELS = ["Mbapp", "Haaland", "Vinicius", "Real Madrid", "Barcelona",
         "Atletico Madrid", "Manchester United", "Liverpool", "Bayern",
         "Premier League", "Champions League", "La Liga", "Serie A"]

ok, ko = 0, []


def verif(nom, condition, detail=""):
    global ok
    if condition:
        ok += 1
    else:
        ko.append((nom, detail))
        print("  ECHEC ", nom, " ", detail)


def attendus(**criteres):
    """Recalcul INDEPENDANT du filtre, depuis la source. Ce code ne partage
    rien avec celui de la page : c'est ce qui lui permet de la contredire."""
    sortie = []
    for j in DONNEES["joueurs"]:
        if "poste" in criteres and j["poste_code"] != criteres["poste"]:
            continue
        if "pays" in criteres and j["pays"] != criteres["pays"]:
            continue
        if "pied" in criteres and j["pied"] != criteres["pied"]:
            continue
        if "age_min" in criteres and j["age"] < criteres["age_min"]:
            continue
        if "age_max" in criteres and j["age"] > criteres["age_max"]:
            continue
        if "taille_min" in criteres and j["taille"] < criteres["taille_min"]:
            continue
        if "valeur_max" in criteres and j["valeur"] > criteres["valeur_max"]:
            continue
        if "buts_min" in criteres and j["buts"] < criteres["buts_min"]:
            continue
        if "fin" in criteres and j["fin_contrat"] != criteres["fin"]:
            continue
        if criteres.get("dispo") and not j["disponible"]:
            continue
        sortie.append(j)
    return sortie


with sync_playwright() as p:
    nav = p.chromium.launch()
    pg = nav.new_page()
    pg.set_viewport_size({"width": 1280, "height": 900})
    erreurs = []
    pg.on("pageerror", lambda e: erreurs.append(str(e)))
    pg.on("console", lambda m: erreurs.append(m.text) if m.type == "error" else None)

    # ---- 1. les pages repondent, et se declarent -------------------------
    for f in PAGES:
        r = pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        verif(f"{f} : repond 200", r.status == 200, str(r.status))
        corps = pg.inner_text("body")
        verif(f"{f} : le bandeau de maquette est present",
              "Mockup." in corps and "invented" in corps)
        verif(f"{f} : noindex",
              pg.evaluate("() => !!document.querySelector('meta[name=robots]')"))
        for reel in REELS:
            verif(f"{f} : ne nomme pas « {reel} »", reel.lower() not in corps.lower())

    # ---- 2. LES LIGUES, PUIS LES CLUBS -----------------------------------
    # C'est l'ordre demande par le client (« il faut les ligues, ensuite les
    # clubs »), et c'est aussi la structure du sport : un club appartient a UN
    # championnat, et c'est ce qui donne un sens au mot « premier ».
    pg.goto(f"{BASE}/competitions.html", wait_until="networkidle")
    cartes = pg.evaluate("""() => [...document.querySelectorAll('.carte')].map(
        a => a.getAttribute('href'))""")
    verif("competitions : toutes les competitions sont listees",
          len(cartes) == len(DONNEES["ligues"]),
          f'{len(cartes)} vs {len(DONNEES["ligues"])}')

    for ligue in DONNEES["ligues"]:
        pg.goto(f"{BASE}/league-{ligue['cle']}.html", wait_until="networkidle")
        corps = pg.inner_text("body")
        rangs = pg.evaluate("""() => [...document.querySelectorAll('.tab tbody tr')].map(
            tr => [...tr.querySelectorAll('td')].map(td => td.textContent.trim()))""")

        if ligue["type"] == "coupe":
            # Une coupe se joue en elimination directe : un tableau de
            # classement y serait faux SUR LE FOND, pas seulement vide.
            verif(f"{ligue['cle']} : la coupe n'affiche aucun classement",
                  len(rangs) == 0, f"{len(rangs)} lignes")
            verif(f"{ligue['cle']} : la page explique pourquoi",
                  "knockout" in corps.lower())
            continue

        table = DONNEES["classements"][ligue["cle"]]
        verif(f"{ligue['cle']} : le classement compte les clubs de la ligue",
              len(rangs) == len(table), f"{len(rangs)} vs {len(table)}")
        clubs_ligue = {club["nom"] for club in DONNEES["clubs"]
                       if club["ligue"] == ligue["cle"]}
        noms_table = {r[1] for r in rangs}
        verif(f"{ligue['cle']} : le classement ne contient QUE ses clubs",
              noms_table <= clubs_ligue,
              str(sorted(noms_table - clubs_ligue)[:3]))
        for r in rangs:
            p_, w, d, lo, gf, ga, gd, pts = (int(x.replace("+", "")) for x in r[2:10])
            verif(f"{ligue['cle']} {r[1][:16]} : joues = V+N+D", p_ == w + d + lo,
                  f"{p_} vs {w}+{d}+{lo}")
            verif(f"{ligue['cle']} {r[1][:16]} : points = 3V+N", pts == 3 * w + d,
                  f"{pts} vs {3 * w + d}")
            verif(f"{ligue['cle']} {r[1][:16]} : GD = GF-GA", gd == gf - ga,
                  f"{gd} vs {gf - ga}")

        # AU NIVEAU DE LA LIGUE, lu dans le tableau AFFICHE. Chaque ligne peut
        # s'additionner correctement et la ligue rester impossible : c'etait le
        # cas de la premiere version, 24 journees pour huit clubs et 52
        # victoires contre 93 defaites. Un lecteur de football le voit tout de
        # suite.
        col = lambda i: [int(r[i].replace("+", "")) for r in rangs]
        verif(f"{ligue['cle']} : autant de victoires que de defaites dans la ligue",
              sum(col(3)) == sum(col(5)), f"{sum(col(3))} V vs {sum(col(5))} D")
        verif(f"{ligue['cle']} : le total des nuls est pair",
              sum(col(4)) % 2 == 0, str(sum(col(4))))
        verif(f"{ligue['cle']} : les buts marques valent les buts encaisses",
              sum(col(6)) == sum(col(7)), f"{sum(col(6))} vs {sum(col(7))}")
        verif(f"{ligue['cle']} : le nombre de journees tient dans un aller-retour",
              all(j == 2 * (len(rangs) - 1) for j in col(2)),
              f"{set(col(2))} pour {len(rangs)} clubs")

    # Un club n'apparait que dans le classement de SON championnat.
    vus = {}
    for ligue in DONNEES["ligues"]:
        if ligue["type"] != "championnat":
            continue
        for slug in ligue["clubs"]:
            verif(f"{slug} : n'est que dans un championnat", slug not in vus,
                  f'aussi dans {vus.get(slug)}')
            vus[slug] = ligue["cle"]
    verif("chaque club a un championnat", len(vus) == len(DONNEES["clubs"]),
          f'{len(vus)} vs {len(DONNEES["clubs"])}')

    # La page Clubs les groupe SOUS leur ligue.
    pg.goto(f"{BASE}/clubs.html", wait_until="networkidle")
    titres = pg.evaluate("() => [...document.querySelectorAll('.sec-h h2')].map(h => h.textContent.trim())")
    noms_ligues = [l["nom"] for l in DONNEES["ligues"] if l["type"] == "championnat"]
    verif("clubs : la page groupe les clubs sous chaque championnat",
          all(n in titres for n in noms_ligues), str(titres[:6]))
    verif("clubs : les trente-deux clubs sont la",
          pg.locator(".carte").count() == len(DONNEES["clubs"]),
          str(pg.locator(".carte").count()))

    # Une fiche club renvoie a SA ligue.
    c0 = DONNEES["clubs"][0]
    pg.goto(f"{BASE}/club-{c0['slug']}.html", wait_until="networkidle")
    liens = pg.evaluate("() => [...document.querySelectorAll('a')].map(a => a.getAttribute('href'))")
    verif("fiche club : renvoie vers sa competition",
          f"league-{c0['ligue']}.html" in liens, str(c0["ligue"]))

    # ---- 3. les onglets de scores ----------------------------------------
    pg.goto(f"{BASE}/live.html", wait_until="networkidle")
    for cle, etat in (("live", "live"), ("termine", "termine"), ("avenir", "avenir")):
        pg.click(f'#onglets .onglet[data-f="{cle}"]')
        pg.wait_for_timeout(150)
        vus = pg.evaluate("""() => [...document.querySelectorAll('#liste .match')]
            .filter(m => !m.hidden).map(m => m.dataset.etat)""")
        prevu = [m for m in DONNEES["matchs"] if m["etat"] == etat]
        verif(f"scores : l'onglet « {cle} » montre les bons matchs",
              len(vus) == len(prevu) and all(v == etat for v in vus),
              f"{len(vus)} affiches vs {len(prevu)} attendus")
    pg.click('#onglets .onglet[data-f="all"]')
    pg.wait_for_timeout(150)
    tous = pg.evaluate("""() => [...document.querySelectorAll('#liste .match')]
        .filter(m => !m.hidden).length""")
    verif("scores : l'onglet « all » les montre tous",
          tous == len(DONNEES["matchs"]), f"{tous} vs {len(DONNEES['matchs'])}")

    # ---- 4. LE FILTRE DE RECRUTEMENT -------------------------------------
    pg.goto(f"{BASE}/recruitment.html", wait_until="networkidle")
    pg.wait_for_timeout(300)

    def applique(**champs):
        pg.click("#raz")
        pg.wait_for_timeout(120)
        for ident, valeur in champs.items():
            if ident in ("fPos", "fNat", "fFoot", "fEnd", "fDispo"):
                pg.select_option(f"#{ident}", str(valeur))
            else:
                pg.fill(f"#{ident}", str(valeur))
        pg.wait_for_timeout(220)
        texte = pg.inner_text("#compte")
        n = int(re.search(r"^(\d+)", texte).group(1))
        noms = pg.evaluate("""() => [...document.querySelectorAll('#res .jr b')]
            .map(b => b.textContent)""")
        return n, noms, texte

    # a. sans filtre : tout le monde
    n, noms, texte = applique()
    verif("recrutement : sans filtre, tous les joueurs correspondent",
          n == len(DONNEES["joueurs"]), f"{n} vs {len(DONNEES['joueurs'])}")
    verif("recrutement : la liste tronquee dit combien elle cache",
          "not shown" in texte and len(noms) == 40, texte)

    # b. un critere simple
    n, noms, _ = applique(fPos="ST")
    prevu = attendus(poste="ST")
    verif("recrutement : filtre par poste", n == len(prevu), f"{n} vs {len(prevu)}")

    # c. LA COMBINAISON — celle qu'un club taperait vraiment, et la seule qui
    #    puisse reveler un ET traite comme un OU.
    n, noms, _ = applique(fPos="CB", fAgeMin=18, fAgeMax=24, fH=185, fDispo="1")
    prevu = attendus(poste="CB", age_min=18, age_max=24, taille_min=185, dispo=True)
    verif("recrutement : la combinaison du cahier des charges (CB, 18-24, >185, dispo)",
          n == len(prevu), f"{n} vs {len(prevu)}")
    verif("recrutement : chaque joueur affiche satisfait VRAIMENT tous les criteres",
          set(noms) <= {j["nom"] for j in prevu},
          str(sorted(set(noms) - {j["nom"] for j in prevu})[:3]))

    # d. valeur et buts
    n, _, _ = applique(fVal=5, fGoals=3)
    prevu = attendus(valeur_max=5, buts_min=3)
    verif("recrutement : valeur maximale et buts minimum",
          n == len(prevu), f"{n} vs {len(prevu)}")

    # e. fin de contrat + pied
    n, _, _ = applique(fEnd="2026", fFoot="Left")
    prevu = attendus(fin="2026", pied="Left")
    verif("recrutement : fin de contrat et pied",
          n == len(prevu), f"{n} vs {len(prevu)}")

    # f. l'ensemble vide est DIT, pas laisse blanc
    pg.click("#raz"); pg.wait_for_timeout(120)
    pg.select_option("#fPos", "GK")
    pg.fill("#fGoals", "30")
    pg.wait_for_timeout(220)
    verif("recrutement : une recherche sans resultat le dit",
          pg.is_visible("#rien"), "le message reste cache")
    verif("recrutement : et n'affiche aucune ligne",
          pg.locator("#res .jr").count() == 0,
          str(pg.locator("#res .jr").count()))

    # g. le bouton Reset remet tout
    pg.click("#raz"); pg.wait_for_timeout(220)
    n = int(re.search(r"^(\d+)", pg.inner_text("#compte")).group(1))
    verif("recrutement : Reset rend la liste complete",
          n == len(DONNEES["joueurs"]), str(n))

    # ---- 5. une fiche joueur est coherente avec la source ----------------
    j = DONNEES["joueurs"][0]
    pg.goto(f"{BASE}/player-{j['slug']}.html", wait_until="networkidle")
    corps = pg.inner_text("body")
    verif("fiche joueur : le nom est celui de la source", j["nom"] in corps)
    verif("fiche joueur : les buts sont ceux de la source",
          str(j["buts"]) in pg.inner_text(".stats"))
    # inner_text rend le texte TRANSFORME : .tbd porte text-transform:uppercase,
    # donc « To be sourced » se lit « TO BE SOURCED ». Une comparaison sensible
    # a la casse faisait echouer le controle ci-dessous — et, bien pire, faisait
    # PASSER ceux d'apres sans rien mesurer : « To be decided » ne pouvait pas
    # etre trouve non plus, quelle que soit la page. On compare en minuscules.
    bas = corps.lower()
    verif("fiche joueur : le vocabulaire du vide est celui de CE produit",
          VIDE.lower() in bas, VIDE)
    # Et il n'est pas melange avec celui d'un autre produit du client.
    for autre in ("To be decided", "À définir", "à vérifier", "À confirmer",
                  "À fournir", "En attente d'autorisation"):
        verif(f"fiche joueur : n'emprunte pas « {autre} » a un autre produit",
              autre.lower() not in bas)
    # Controle positif de la recherche ci-dessus : elle doit savoir TROUVER un
    # de ces libelles quand il est present. Sans lui, six controles verts ne
    # prouveraient rien du tout.
    verif("fiche joueur : la recherche de vocabulaire sait trouver un libelle",
          "to be sourced" in bas, "la comparaison en minuscules ne trouve rien")

    # ---- 6. mobile --------------------------------------------------------
    for f in ("index.html", "recruitment.html", "player-player-1.html"):
        pg.set_viewport_size({"width": 390, "height": 800})
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        pg.wait_for_timeout(250)
        debord = pg.evaluate("() => document.documentElement.scrollWidth"
                             " - document.documentElement.clientWidth")
        verif(f"{f} : pas de debordement horizontal a 390 px", debord <= 0, str(debord))
    pg.set_viewport_size({"width": 1280, "height": 900})

    # ---- 7. LA COULEUR D'ACCENT -------------------------------------------
    # Demandee en orange par le client le 9 sept (« orange color for the
    # football color », theme noir conserve). On la lit sur la couleur
    # CALCULEE par le navigateur, pas dans la feuille : c'est la seule qui
    # dise quelle regle a gagne.
    ACCENT = "rgb(255, 122, 24)"
    pg.goto(f"{BASE}/live.html", wait_until="networkidle")
    pg.wait_for_timeout(200)
    fond_onglet = pg.evaluate("() => getComputedStyle("
                              "document.querySelector('.onglet[aria-pressed=true]')"
                              ").backgroundColor")
    verif("accent : l'onglet actif est orange", fond_onglet == ACCENT, fond_onglet)
    pg.goto(f"{BASE}/recruitment.html", wait_until="networkidle")
    pg.wait_for_timeout(500)
    coul_compte = pg.evaluate("() => getComputedStyle(document.querySelector('.compte')).color")
    verif("accent : le compteur de resultats est orange", coul_compte == ACCENT, coul_compte)
    # Le theme reste NOIR : il a dit « you already done it with a black theme ».
    fond_page = pg.evaluate("() => getComputedStyle(document.body).backgroundColor")
    verif("accent : le fond reste sombre", fond_page == "rgb(11, 16, 20)", fond_page)

    import urllib.request
    css = urllib.request.urlopen(f"{BASE}/assets/site.css").read().decode("utf-8")
    verif("accent : plus aucune trace du vert d'origine",
          "25D07A" not in css.upper() and "37,208,122" not in css,
          "le vert subsiste dans la feuille")
    # Controle positif : la recherche dans la feuille sait trouver une couleur.
    # Sans lui, une feuille vide ou une URL fausse rendrait le controle
    # ci-dessus vert sans rien avoir lu.
    verif("accent : la feuille lue contient bien l'orange",
          "FF7A18" in css.upper(), f"{len(css)} octets lus")

    # ---- 8. AUCUN LIEN MORT ----------------------------------------------
    # Le jeu de donnees vient de changer (dix clubs -> trente-deux, un
    # classement -> quatre). Des pages de l'ancienne version restaient sur le
    # disque et pointaient vers une page supprimee. Un lien mort dans une
    # maquette fait douter de tout le reste, et il ne se voit qu'en cliquant.
    import urllib.request
    import urllib.error
    liens = set()
    for f in PAGES + ["competitions.html", "clubs.html"]:
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        for href in pg.evaluate("() => [...document.querySelectorAll('a')]"
                                ".map(a => a.getAttribute('href'))"):
            if href and not href.startswith(("http", "#", "mailto:")):
                liens.add(href.split("#")[0])
    morts = []
    for href in sorted(liens):
        try:
            with urllib.request.urlopen(f"{BASE}/{href}") as r:
                if r.status != 200:
                    morts.append((href, r.status))
        except urllib.error.HTTPError as e:
            morts.append((href, e.code))
    verif(f"aucun lien mort parmi les {len(liens)} liens internes rencontres",
          not morts, str(morts[:4]))
    # Controle positif : la sonde sait reconnaitre une page absente. Sans lui,
    # une sonde cassee declarerait « 0 lien mort » sur un site en ruines.
    absent = None
    try:
        urllib.request.urlopen(f"{BASE}/page-qui-nexiste-pas.html")
    except urllib.error.HTTPError as e:
        absent = e.code
    verif("la sonde de liens sait voir une page absente", absent == 404, str(absent))

    verif("aucune erreur JavaScript sur l'ensemble", not erreurs, str(erreurs[:2]))

    # ---- captures ---------------------------------------------------------
    D = "/var/lib/freelancer/projects/40478471/"
    for f, nom in (("index.html", "foot-1-accueil"),
                   ("recruitment.html", "foot-2-recrutement"),
                   ("player-player-1.html", "foot-3-joueur"),
                   ("data.html", "foot-4-donnees")):
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        pg.wait_for_timeout(350)
        pg.screenshot(path=D + nom + ".png")
    pg.set_viewport_size({"width": 390, "height": 800})
    pg.goto(f"{BASE}/recruitment.html", wait_until="networkidle")
    pg.wait_for_timeout(350)
    pg.screenshot(path=D + "foot-5-mobile.png")

    nav.close()

print(f"\n{ok + len(ko)} verifications, {len(ko)} echec(s)")
for nom, detail in ko:
    print("  -", nom, detail)
sys.exit(1 if ko else 0)
