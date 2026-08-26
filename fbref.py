import time
import random
import orodja
import re

seznam_vseh_URL = [
    # LIGE
    "https://fbref.com/en/comps/12/2025-2026/stats/2025-2026-La-Liga-Stats",
    "https://fbref.com/en/comps/9/2025-2026/stats/2025-2026-Premier-League-Stats",
    "https://fbref.com/en/comps/11/2025-2026/stats/2025-2026-Serie-A-Stats",
    "https://fbref.com/en/comps/20/2025-2026/stats/2025-2026-Bundesliga-Stats",
    "https://fbref.com/en/comps/13/2025-2026/stats/2025-2026-Ligue-1-Stats",
    "https://fbref.com/en/comps/32/2025-2026/stats/2025-2026-Primeira-Liga-Stats",
    "https://fbref.com/en/comps/23/2025-2026/stats/2025-2026-Eredivisie-Stats",
    "https://fbref.com/en/comps/26/2025-2026/stats/2025-2026-Super-Lig-Stats",
    "https://fbref.com/en/comps/10/2025-2026/stats/2025-2026-Championship-Stats",
    "https://fbref.com/en/comps/70/2025-2026/stats/2025-2026-Saudi-Pro-League-Stats",
    "https://fbref.com/en/comps/22/2025/stats/2025-Major-League-Soccer-Stats",
    "https://fbref.com/en/comps/24/2025/stats/2025-Serie-A-Stats",
    "https://fbref.com/en/comps/37/2025-2026/stats/2025-2026-Belgian-Pro-League-Stats",
    "https://fbref.com/en/comps/17/2025-2026/stats/2025-2026-Segunda-Division-Stats",
    "https://fbref.com/en/comps/30/2025-2026/stats/2025-2026-Russian-Premier-League-Stats",
    "https://fbref.com/en/comps/27/2025-2026/stats/2025-2026-Super-League-Greece-Stats",
    "https://fbref.com/en/comps/54/2025-2026/stats/2025-2026-Serbian-SuperLiga-Stats",
    "https://fbref.com/en/comps/31/2025-2026/stats/2025-2026-Liga-MX-Stats",
    # EVROPSKA KLUBSKA TEKMOVANJA
    "https://fbref.com/en/comps/8/2025-2026/stats/2025-2026-Champions-League-Stats",
    "https://fbref.com/en/comps/19/2025-2026/stats/2025-2026-Europa-League-Stats",
    "https://fbref.com/en/comps/882/2025-2026/stats/2025-2026-Conference-League-Stats",
    # OSTALA MEDNARODNA KLUBSKA TEKMOVANJA
    "https://fbref.com/en/comps/14/2025/stats/2025-Copa-Libertadores-Stats",
    "https://fbref.com/en/comps/205/2025/stats/2025-Copa-Sudamericana-Stats",
    "https://fbref.com/en/comps/133/2025/stats/2025-CONCACAF-Champions-Cup-Stats",
    "https://fbref.com/en/comps/939/2025/stats/2025-Leagues-Cup-Stats",
    # ANGLIJA
    "https://fbref.com/en/comps/514/2025-2026/stats/2025-2026-FA-Cup-Stats",
    "https://fbref.com/en/comps/690/2025-2026/stats/2025-2026-EFL-Cup-Stats",
    # ŠPANIJA
    "https://fbref.com/en/comps/569/stats/Copa-del-Rey-Stats",
    "https://fbref.com/en/comps/646/stats/Supercopa-de-Espana-Stats",
    # FRANCIJA
    "https://fbref.com/en/comps/518/stats/Coupe-de-France-Stats",
    # NEMČIJA
    "https://fbref.com/en/comps/521/2025-2026/stats/2025-2026-DFB-Pokal-Stats",
    # ITALIJA
    "https://fbref.com/en/comps/529/2025-2026/stats/2025-2026-Coppa-Italia-Stats",
    "https://fbref.com/en/comps/612/stats/Supercoppa-Italiana-Stats",
    # ZDA
    "https://fbref.com/en/comps/577/2025/stats/2025-US-Open-Cup-Stats",
]
# mapa v kateri bodo shranjeni podatki
fbref_mapa = "podatki/fbref"


# Iz URL-ja pridobi poenostavljeno ime tekmovanja, ki ga uporabljamo pri imenovanju datotek.
def ime_tekmovanja_iz_url(url):
    # Brazilska Serie A ima enako kot italijanska, zato jo poimenujemo posebej
    if "/comps/24/" in url:
        return "serie_a_bra"

    ujemanje = re.search(r"/stats/(?:\d{4}(?:-\d{4})?-)?(.*?)-Stats/?$", url)
    tekmovanje = ujemanje.group(1)
    return tekmovanje.lower().replace("-", "_")


# Prenese strani vseh ibranih FBref tekmovanj in preveri, ali je preneseni HTML veljaven, preden ga shrani.
# Prihajalo je do Cloudflare blokade. Tam se je pojavil HTML, ki sem ga izluščil za preverjanje veljavnosti HTML-ja.
def prenos_strani_fbref():
    for i, URL in enumerate(seznam_vseh_URL, 1):
        ime_tekmovanja = ime_tekmovanja_iz_url(URL)
        ime_datoteke = f"stran_fbref_{ime_tekmovanja}.html"

        # Veljavne že prenesene strani preskočimo.
        if orodja.datoteka_obstaja(fbref_mapa, ime_datoteke):
            continue

        odgovor = orodja.prenesi_stran_selenium(URL)

        if odgovor is None:
            print("Prenos ni uspel:", i)
            continue

        orodja.shrani_niz_v_datoteko(odgovor, fbref_mapa, ime_datoteke)

        print("Uspešno prenesena stran:", i)

        time.sleep(random.uniform(5, 8))


# Prvotno sem želel prenesti profil vsakega igralca posebej, vendar bi to zahtevalo več tisoč zahtevkov, pri katerih je FBref sprožil Cloudflare zaščito (pomagal ni niti time.sleep()).
# Zato podatke pridobivamo neposredno iz tabel posameznih tekmovanj.


# Iz HTML tabele izloči posamezne vrstice, kjer vsaka vrstica predstavlja enega igralca.
def stran_v_blok(besedilo):
    return re.findall(
        r'<tr >.*?data-stat="ranker" >.*?</td></tr>', besedilo, flags=re.DOTALL
    )


# Iz HTML-bloka posameznega igralca izlušči ID, ime in statistiko ter podatke vrne v obliki slovarja.
def izlusci_podatke_igralca(blok, tekmovanje):
    fbref_id = re.search(r'data-append-csv="(.*?)"', blok)
    ime = re.search(r'<a href="/en/players/.*?/.*?">(.*?)</a>', blok)
    tekme = re.search(r'data-stat="games" >(\d+)</td>', blok)
    minute = re.search(r'data-stat="minutes" csk="(\d+)" >.*?</td>', blok)
    goli = re.search(r'data-stat="goals" >(\d+)</td>', blok)
    asistence = re.search(r'data-stat="assists" >(\d+)</td>', blok)
    goli_in_asistence = re.search(r'data-stat="goals_assists" >(\d+)</td>', blok)

    # Če kateri od obveznih podatkov manjka, igralca izpustimo.
    if any(
        x is None
        for x in [
            fbref_id,
            ime,
            tekme,
            minute,
            goli,
            asistence,
            goli_in_asistence,
        ]
    ):
        return None

    return {
        "fbref_id": fbref_id.group(1),
        "ime": ime.group(1),
        "tekmovanje": tekmovanje,
        "tekme": int(tekme.group(1)),
        "min": int(minute.group(1)),
        "goli": int(goli.group(1)),
        "asistence": int(asistence.group(1)),
        "G+A": int(goli_in_asistence.group(1)),
    }


# Zdrži statistikoistega igralca iz različnih tekmovanj na podlaki fbref_id ter sešteje njegove minute, gole in asistence.
def zdruzi_igralce_po_fbref_id(igralci):
    zdruzeni_igralci = {}

    for igralec in igralci:
        fbref_id = igralec["fbref_id"]

        # Ob prvem pojavu igralca ustvarimo nov zapis.
        if fbref_id not in zdruzeni_igralci:
            zdruzeni_igralci[fbref_id] = {
                "fbref_id": fbref_id,
                "ime": igralec["ime"],
                "tekmovanja": [igralec["tekmovanje"]],
                "tekme": igralec["tekme"],
                "min": igralec["min"],
                "goli": igralec["goli"],
                "asistence": igralec["asistence"],
                "G+A": igralec["G+A"],
            }

        # Pri naslednjih pojavitvah prištejemo statistiko iz dodatnega tekmovanja.
        else:
            zdruzen_igralec = zdruzeni_igralci[fbref_id]
            zdruzen_igralec["tekme"] += igralec["tekme"]
            zdruzen_igralec["min"] += igralec["min"]
            zdruzen_igralec["goli"] += igralec["goli"]
            zdruzen_igralec["asistence"] += igralec["asistence"]
            zdruzen_igralec["G+A"] += igralec["G+A"]

            if igralec["tekmovanje"] not in zdruzen_igralec["tekmovanja"]:
                zdruzen_igralec["tekmovanja"].append(igralec["tekmovanje"])

    return list(zdruzeni_igralci.values())


# Copilot: s pomočjo dobil idejo za združevanje podatkov.


# Iz ene HTML-datoteke pripravi seznam veljavnih igralcev.
def igralci_iz_datoteke(mapa, datoteka, url):
    vsebina = orodja.preberi_datoteko_v_niz(mapa, datoteka)
    bloki = stran_v_blok(vsebina)

    tekmovanje = ime_tekmovanja_iz_url(url)
    igralci = [izlusci_podatke_igralca(blok, tekmovanje) for blok in bloki]

    return [igralec for igralec in igralci if igralec is not None]


def zapisi_igralce_v_csv(igralci, mapa, datoteka):
    # Preverimo, da imajo vsi zapisi igralcev enake stolpce.
    assert igralci and (all(igralec.keys() == igralci[0].keys() for igralec in igralci))
    vrstice = list(igralci[0].keys())
    orodja.zapisi_csv(vrstice, igralci, mapa, datoteka)


# Izvede celoten postopek prenosa, obdelave, združevanja in shranjevanja podatkov.
def main():
    prenos_strani_fbref()

    koncni_seznam_vseh_igralcev = []

    for URL in seznam_vseh_URL:
        tekmovanje = ime_tekmovanja_iz_url(URL)
        ime_datoteke = f"stran_fbref_{tekmovanje}.html"

        igralci = igralci_iz_datoteke(fbref_mapa, ime_datoteke, URL)

        koncni_seznam_vseh_igralcev.extend(igralci)

    zdruzeni_igralci = zdruzi_igralce_po_fbref_id(koncni_seznam_vseh_igralcev)

    zapisi_igralce_v_csv(zdruzeni_igralci, fbref_mapa, "fbref_igralci.csv")


if __name__ == "__main__":
    main()
