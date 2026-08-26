import orodja
import time
import random
import re


opta_mapa = "podatki/opta"

opta_URL = {
    "lige": "https://dataviz.theanalyst.com/opta-power-rankings/?leagueRankings=true&limit=350",
    "champions_league": "https://theanalyst.com/competition/uefa-champions-league/power-rankings",
    "europa_league": "https://theanalyst.com/competition/uefa-europa-league/power-rankings",
    "conference_league": "https://theanalyst.com/competition/uefa-conference-league/power-rankings",
}
# FIFA Club World Cup sem izbrisal zato, ker na spletni strani Opta Analyst ni bilo podatkov o sodelujočih ekipah.
# To tekmovanje sem izbrisal tudi iz fbref_igralci.csv


# Prenese strani Opta Analyst z močmi lig in evropskih tekmovanj ter njihov HTML shrani v mapo podatki/opta
def prenos_strani_opta():
    for ime, URL in opta_URL.items():
        ime_datoteke = f"stran_opta_{ime}.html"

        if orodja.datoteka_obstaja(opta_mapa, ime_datoteke):
            continue

        prenos = orodja.prenesi_stran_selenium_dom(URL)

        if prenos is None:
            print("Prenos ni uspel", ime)
            continue

        odgovor = prenos.replace("</tr><tr", "</tr>\n<tr>")

        # HTML strani se je prenesel tako, da je bila celotna tabela v eni vrstici, zato med vrsticami tabele dodamo prelome vrstic za bolj pregleden zapis.

        orodja.shrani_niz_v_datoteko(odgovor, opta_mapa, ime_datoteke)

        time.sleep(random.uniform(2, 4))


# Prebere shranjeno HTML datoteko in s pomočjo regularnih izrazov izlušči imena lig ter njihobe pripadajoče ocene (moči).
def izlusci_moc_lig():
    vsebina = orodja.preberi_datoteko_v_niz(opta_mapa, "stran_opta_lige.html")
    moc_lig = {}

    for zadetek in re.finditer(
        r'"nation logo">(.*?)<.*?padding-left: 8px;">(.*?)<', vsebina
    ):
        liga = zadetek.group(1)
        moc = float(zadetek.group(2))

        moc_lig[liga] = moc

    return moc_lig


# Izračuna povprečno moč tekmovanja glede na moč lig iz katerih prihajajo sodelujoči klubi.
def izracun_moci_tekmovanja(sestava, moc_lig):
    vsota = 0
    stevilo_klubov = 0

    for liga, stevilo in sestava.items():
        vsota += moc_lig[liga] * stevilo
        stevilo_klubov += stevilo

    return vsota / stevilo_klubov


sestava_url = {
    "copa_libertadores": "https://en.wikipedia.org/wiki/2025_Copa_Libertadores#Group_stage",
    "copa_sudamericana": "https://en.wikipedia.org/wiki/2025_Copa_Sudamericana",
    "concacaf_champions_cup": "https://en.wikipedia.org/wiki/2026_CONCACAF_Champions_Cup",
    "leagues_cup": "https://en.wikipedia.org/wiki/2026_Leagues_Cup",
    "fa_cup": "https://en.wikipedia.org/wiki/2025%E2%80%9326_FA_Cup",
    "efl_cup": "https://en.wikipedia.org/wiki/2025%E2%80%9326_EFL_Cup",
    "copa_del_rey": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Copa_del_Rey",
    "supercopa_de_espana": "https://en.wikipedia.org/wiki/2026_Supercopa_de_Espa%C3%B1a",
    "coupe_de_france": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Coupe_de_France",
    "dfb_pokal": "https://en.wikipedia.org/wiki/2025%E2%80%9326_DFB-Pokal",
    "coppa_italiana": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Coppa_Italia",
    "supercoppa_italiana": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Supercoppa_Italiana",
    "us_open_cup": "https://en.wikipedia.org/wiki/2026_U.S._Open_Cup",
}


# Prenese strani iz slovarja sestava_url. To so tekmovanja v katerih so igralii igralci, ki so med 500 najvrednejšimi in niso lige.
def prenos_sestav_tekmovanj():
    for tekmovanje, URL in sestava_url.items():
        ime_datoteke = f"sestava_{tekmovanje}.html"

        if orodja.datoteka_obstaja(opta_mapa, ime_datoteke):
            continue

        odgovor = orodja.prenesi_stran(URL)

        if odgovor is None:
            print("Prenos ni uspel:", tekmovanje)
            continue

        orodja.shrani_niz_v_datoteko(odgovor, opta_mapa, ime_datoteke)


tipi_sestav = {
    "fa_cup": "zip",
    "efl_cup": "zip",
    "copa_del_rey": "opis",
    "coppa_italiana": "participating",
    "dfb_pokal": "participating_dfb",
    "coupe_de_france": "france",
    "us_open_cup": "usa",
    "leagues_cup": "leagues_cup",
    "copa_libertadores": "drzave",
    "copa_sudamericana": "drzave",
    "concacaf_champions_cup": "concacaf",
}

# tekmovanja, pri katerih sestavo poznamo brez luščenja HTML-ja
posebne_sestave = {
    "supercopa_de_espana": {"La Liga": 4},
    "supercoppa_italiana": {"Serie A": 4},
}

# Del HTML-ja kjer se nahajajo ekipe, ki so tekmovale v teh dveh tekmovanjih.
odseki_zip = {
    "fa_cup": ("Third_round", "Fourth_round"),
    "efl_cup": ("Second_round", "Third_round"),
}

# Del HTML-ja, kjer se nahajajo ekipe, ki so tekmovale v tem tekmovanju.
odseki_opis = {"copa_del_rey": ("Round_of_32", "Round_of_16")}

# Za tekmovanje CONCACAF Champions cup sem izluščil državo in jo potem preimenoval v ime lige, kot je na Opta Analyst.
lige_concacaf = {
    "Jamaica": "Jamaica Premier League",
    "Costa Rica": "Costa Rica Primera Division",
    "United States": "Major League Soccer",
    "Mexico": "Liga MX",
    "Canada": "Canadian Premier League",
    "Dominican Republic": "Dominican Republic Liga",
    "Trinidad and Tobago": "Trinidad and Tobago Premier League",
    "Guatemala": "Guatemala Liga Nacional",
    "Honduras": "Honduras Liga Nacional",
    "Panama": "Panama Liga",
}

# Imena tekmovanj na Wikipediji in Opta Analyst se razlikujejo, zato jih preimenujemo
preimenovanja_lig = {
    # Južna Amerika
    "Brazil": "Brazilian Serie A",
    "Argentina": "Liga Profesional Argentina",
    "Uruguay": "Uruguay Liga AUF",
    "Paraguay": "Paraguay Primera División",
    "Ecuador": "Ecuador Liga Pro",
    "Chile": "Chile Primera",
    "Bolivia": "Bolivia Primera División",
    "Colombia": "Colombia Primera A",
    "Peru": "Peru Liga 1",
    "Venezuela": "Venezuela Primera División",
    # CONCACAF
    "Jamaica Premier League": "Premier League",
    "Panama Liga": "LPF",
    # Severna Amerika
    "Major League Soccer": "US Major League Soccer",
    "Liga MX": "Mexican Primera",
    # Anglija
    "Premier League": "English Premier League",
    "Championship": "English Championship",
    "League One": "English League One",
    "League Two": "English League Two",
    # Španija
    "La Liga": "Spanish La Liga",
    "Segunda División": "Spanish Segunda Division",
    "Primera Federación": "Spanish Primera Division RFEF",
    "Segunda Federación": "Spanish Segunda Division RFEF",
    # Francija
    "Ligue 1": "French Ligue 1",
    "Ligue 2": "French Ligue 2",
    "Ligue 3": "French Ligue 3",
    # Nemčija
    "Bundesliga": "German Bundesliga",
    "2. Bundesliga": "German Bundesliga Zwei",
    "3. Liga": "German 3rd Liga",
    # Italija
    "Serie A": "Italian Serie A",
    "Serie B": "Italian Serie B",
    "Serie C": "Italian Serie C",
}


def izloci_sestavo(tekmovanje):

    # posebni primer
    if tekmovanje in posebne_sestave:
        return posebne_sestave[tekmovanje]

    vsebina = orodja.preberi_datoteko_v_niz(opta_mapa, f"sestava_{tekmovanje}.html")

    tip = tipi_sestav[tekmovanje]
    sestava = {}

    # FA Cup, EFL Cup
    if tip == "zip":
        zacetek, konec = odseki_zip[tekmovanje]

        blok = re.search(
            rf'<h2 id="{zacetek}">.*?<h2 id="{konec}">', vsebina, re.DOTALL
        ).group()

        tabela = re.search(
            r'<table class="wikitable".*?</table>', blok, re.DOTALL
        ).group()

        lige = re.findall(r"<th[^>]*>([^<]+).*?</th>", tabela, re.DOTALL)

        stevila = re.findall(r'<span class="nowrap">\s*(\d+)\s*/', tabela)

        for liga, stevilo in zip(lige, stevila):
            # "Total" ni liga, zato ga ne shranimo.
            if liga != "Total":
                sestava[liga] = int(stevilo)
    # Copilot: Pomagal s sestavo regularnega izraza.

    # Copa del rey
    elif tip == "opis":
        zacetek, konec = odseki_opis[tekmovanje]

        blok = re.search(
            rf'<h2 id="{zacetek}">.*?<h2 id="{konec}">', vsebina, re.DOTALL
        ).group()

        tabela = re.search(
            r'<table class="wikitable".*?</table>', blok, re.DOTALL
        ).group()

        vzorec = (
            r">(\d+)\s+"
            r"(?:participants in|teams? of)\s*"
            r"<a[^>]*>([^<]+)</a></span>"
        )

        for stevilo, liga in re.findall(vzorec, tabela):
            stevilo = int(stevilo)

            if liga == "2026 Supercopa de España":
                liga = "La Liga"

            elif liga == "Copa Federación":
                liga = "Primera Federación"

            if liga in sestava:
                sestava[liga] += stevilo
            else:
                sestava[liga] = stevilo

    # Coppa Italiana
    elif tip == "participating":
        blok = re.search(
            r'<h2 id="Participating_teams">.*?<h2 id="First_stage">', vsebina, re.DOTALL
        ).group()

        vzorec = (
            r"<b[^>]*>(Serie [ABC])</b>"
            r"<br[^>]*/>"
            r"(?:The )?(\d+|Four) clubs"
        )

        for liga, stevilo in re.findall(vzorec, blok):
            if stevilo == "Four":
                stevilo = 4
            else:
                stevilo = int(stevilo)

            sestava[liga] = stevilo

    # DFB pokal
    elif tip == "participating_dfb":
        blok = re.search(
            r'<h2 id="Participating_clubs">.*?<h2 id="Format">', vsebina, re.DOTALL
        ).group()
        sestava["Bundesliga"] = 18
        sestava["2. Bundesliga"] = 18
        sestava["3. Liga"] = 4

    # Coupe de France
    elif tip == "france":
        sestava["Ligue 1"] = 15
        sestava["Ligue 2"] = 8
        sestava["Ligue 3"] = 3
        sestava["National 1"] = 3

    # US open cup
    elif tip == "usa":
        tabela = re.search(
            r'<table class="wikitable"[^>]*>'
            r".*?Teams for Round of 32 draw"
            r".*?</table>",
            vsebina,
            re.DOTALL,
        ).group()

        stolpci = re.findall(r"<td[^>]*>(.*?)</td>", tabela, re.DOTALL)

        kratice = re.findall(r"\((USLC|USL1|MLSNP)\)", stolpci[0])

        pretvorbe_usa = {
            "USLC": "USL Championship",
            "USL1": "USL League One",
            "MLSNP": "MLS Next Pro",
        }

        for kratica in kratice:
            liga = pretvorbe_usa[kratica]

            if liga in sestava:
                sestava[liga] += 1
            else:
                sestava[liga] = 1

        sestava["Major League Soccer"] = 16

    # Leagues cup
    elif tip == "leagues_cup":
        blok = re.search(r'<h2 id="Teams">.*?<h3 id="Draw"', vsebina, re.DOTALL).group()
        zadetek = re.search(
            r"all (\d+) Liga MX teams and (\d+) out of \d+ MLS teams", blok
        )

        sestava["Liga MX"] = int(zadetek.group(1))
        sestava["Major League Soccer"] = int(zadetek.group(2))

    # Copa libertadores, Copa sudamericana
    # Izluščil države, iz katerih so klubi in jih nato preimenoval v lige.
    elif tip == "drzave":
        tabela = re.search(
            r"<caption>Group stage draw</caption>.*?</table>", vsebina, re.DOTALL
        ).group()

        drzave = re.findall(r'<img alt="([^"]+)"', tabela)

        for drzava in drzave:
            if drzava in sestava:
                sestava[drzava] += 1
            else:
                sestava[drzava] = 1

    # CONCACAF champions cup
    elif tip == "concacaf":
        blok = re.search(
            r'<h2 id="Teams">.*?<h2 id="Draw">', vsebina, re.DOTALL
        ).group()

        vzorec = (
            r'<span class="flagicon".*?'
            r'<img alt="([^"]+)".*?'
            r"</span></span>\s*"
            r"<a[^>]*>([^<]+)</a>"
        )
        # Copilot: Pomagal pri oblikovanju regularnega izraza.

        for drzava, klub in re.findall(vzorec, blok, re.DOTALL):
            if klub == "Vancouver Whitecaps FC":
                liga = "Major League Soccer"
            else:
                liga = lige_concacaf[drzava]

            if liga in sestava:
                sestava[liga] += 1
            else:
                sestava[liga] = 1

    return sestava


izkljucene_lige = {
    "Dominican Republic Liga",
    "Trinidad and Tobago Premier League",
    "Non-League",
}


def preimenuj_lige(sestava):
    nova_sestava = {}

    for liga, stevilo in sestava.items():
        if liga in izkljucene_lige:
            continue

        novo_ime = preimenovanja_lig.get(liga, liga)

        if novo_ime in nova_sestava:
            nova_sestava[novo_ime] += stevilo
        else:
            nova_sestava[novo_ime] = stevilo

    return nova_sestava


def moc_tekmovanja_iz_datoteke(tekmovanje, moc_lig):
    sestava = izloci_sestavo(tekmovanje)
    sestava = preimenuj_lige(sestava)

    moc = izracun_moci_tekmovanja(sestava, moc_lig)

    return {"tekmovanje": tekmovanje, "moc": round(moc, 2)}


def izlusci_moc_evropskega_tekmovanja(tekmovanje):
    vsebina = orodja.preberi_datoteko_v_niz(opta_mapa, f"stran_opta_{tekmovanje}.html")

    moci = re.findall(
        r'alt="team logo"[^>]*>.*?</span>'
        r".*?</td>"
        r'<td class="Table-module_number-cell__[^"]*">.*?</td>'
        r'<td class="Table-module_number-cell__[^"]*">(\d+(?:\.\d+)?)</td>',
        vsebina,
        re.DOTALL,
    )

    moci = [float(moc) for moc in moci]

    return sum(moci) / len(moci)


def zapisi_moci_tekmovanj_v_csv(tekmovanja, mapa, datoteka):
    assert tekmovanja and all(
        tekmovanje.keys() == tekmovanja[0].keys() for tekmovanje in tekmovanja
    )

    stolpci = list(tekmovanja[0].keys())
    orodja.zapisi_csv(stolpci, tekmovanja, mapa, datoteka)


def main():
    prenos_strani_opta()
    prenos_sestav_tekmovanj()

    moc_lig = izlusci_moc_lig()

    moci_tekmovanj = []

    for liga, moc in moc_lig.items():
        moci_tekmovanj.append({"tekmovanje": liga, "moc": round(moc, 2)})

    for tekmovanje in tipi_sestav:
        podatek = moc_tekmovanja_iz_datoteke(tekmovanje, moc_lig)
        moci_tekmovanj.append(podatek)

    for tekmovanje in posebne_sestave:
        podatek = moc_tekmovanja_iz_datoteke(tekmovanje, moc_lig)
        moci_tekmovanj.append(podatek)

    for tekmovanje in opta_URL:
        if tekmovanje == "lige":
            continue
        moc = izlusci_moc_evropskega_tekmovanja(tekmovanje)
        moci_tekmovanj.append({"tekmovanje": tekmovanje, "moc": round(moc, 2)})

    zapisi_moci_tekmovanj_v_csv(moci_tekmovanj, opta_mapa, "moc_tekmovanj.csv")


if __name__ == "__main__":
    main()
