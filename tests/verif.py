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

from donnees import DONNEES, VIDE

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8921").rstrip("/")

PAGES = ["index.html", "live.html", "players.html", "clubs.html",
         "standings.html", "recruitment.html", "data.html",
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

    # ---- 2. le classement s'additionne -----------------------------------
    pg.goto(f"{BASE}/standings.html", wait_until="networkidle")
    lignes = pg.evaluate("""() => [...document.querySelectorAll('.tab tbody tr')].map(
        tr => [...tr.querySelectorAll('td')].map(td => td.textContent.trim()))""")
    verif("classement : autant de lignes que de clubs classes",
          len(lignes) == len(DONNEES["classement"]), str(len(lignes)))
    for l in lignes:
        # colonnes : rang, club, P, W, D, L, GF, GA, GD, Pts
        p_, w, d, lo, gf, ga, gd, pts = (int(x.replace("+", "")) for x in l[2:10])
        verif(f"classement {l[1][:18]} : joues = V+N+D", p_ == w + d + lo,
              f"{p_} vs {w}+{d}+{lo}")
        verif(f"classement {l[1][:18]} : points = 3V+N", pts == 3 * w + d,
              f"{pts} vs {3 * w + d}")
        verif(f"classement {l[1][:18]} : difference = GF-GA", gd == gf - ga,
              f"{gd} vs {gf - ga}")

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
