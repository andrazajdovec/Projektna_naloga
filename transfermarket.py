import time
import random
import orodja
import re

# URL glavne strani Transfermarketa#
tm_URL = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page="
# mapa v kateri bodo shranjeni podatki#
tm_directory = "podatki/transfermarket"


def prenos_strani_tm():
    for i in range(1, 21):
        if orodja.datoteka_obstaja(tm_directory, f"stran_tm{i}.html") is True:
            continue

        odgovor = orodja.prenesi_stran(f"{tm_URL}{i}")
        if odgovor is None:
            print("napaka", i)
            continue

        orodja.shrani_niz_v_datoteko(odgovor, tm_directory, f"stran_tm{i}.html")

        time.sleep(random.uniform(2, 5))
        # GEMINI


# funkcija poišče posameznega igralca na spletni strani in vrne seznam igralcev#
def stran_v_blok(besedilo):
    return re.findall(
        r'<tr class="(?:odd|even)">.*?(?=<tr class="(?:odd|even)">|$)',
        besedilo,
        flags=re.DOTALL,
    )
    # GEMINI IN NAPAKA ZARADI KATERE NI DELOVALA SKRIPTA


# (?:odd|even)
# Oklepaji () v regexu običajno pomenijo "ujemi ta del in mi ga vrni posebej".
# Če dodaš ?: na začetek oklepaja ((?:...)), pa Pythonu rečeš: "Uporabi oklepaje
# samo zato, da združiš možnost odd ali even, ampak mi tega teksta ne shranjuj kot poseben ujet podatek."

# (?=...)
# To je tisti del, ki povzroča največ preglavic. Konstrukcija (?=neki_tekst) pomeni:
# "Preveri, ali v besedilu takoj za mano sledi neki_tekst,
# ampak tega neki_tekst-a ne vključi v rezultat in ne porabi v iskanju."
# V tvojem primeru (?=<tr class="(?:odd|even)">|$) reče:
# "Pobiraj vse znake naprej, dokler tik pred sabo ne vidiš začetka naslednjega igralca ali pa konca datoteke ($)."


# pomožna funkcija, ki vse vrednosti pretvori v milijone in v float#
def pretvori_vrednost(vrednost):
    if "m" in vrednost:
        return float(vrednost[:-1])
    elif "k" in vrednost:
        return float(vrednost[:-1]) / 1000


def izlusci_podatke_igralca(blok):
    uvrstitev = re.search(r'<td class="zentriert">(\d+)</td>', blok)
    ime = re.search(r'<td class="hauptlink"><a .*?>(.*?)</a>', blok)
    starost = re.search(r'</td><td class="zentriert">(\d+)</td>', blok)
    drzavljanstvo = re.search(
        r'<td class="zentriert"><img src=.*?title="(.*?)" alt=', blok
    )
    klub = re.search(r'<td class="zentriert"><a title="(.*?)" href="/', blok)
    vrednost = re.search(r'<a href="/.*?>€(.*?)</a>', blok)

    if (
        uvrstitev == None
        or ime == None
        or starost == None
        or drzavljanstvo == None
        or klub == None
        or vrednost == None
    ):
        return None
    return {
        "uvrstitev": int(uvrstitev.group(1)),
        "ime": ime.group(1),
        "starost": int(starost.group(1)),
        "drzavljanstvo": drzavljanstvo.group(1),
        "klub": klub.group(1),
        "vrednost": pretvori_vrednost(vrednost.group(1)),
    }


def igralci_iz_datoteke(mapa, datoteka):
    vsebina = orodja.preberi_datoteko_v_niz(mapa, datoteka)
    bloki = stran_v_blok(vsebina)
    igralci = [izlusci_podatke_igralca(blok) for blok in bloki]
    return [igralec for igralec in igralci if igralec != None]


def zapisi_igralce_v_csv(igralci, mapa, datoteka):
    assert igralci and (all(igralec.keys() == igralci[0].keys() for igralec in igralci))
    vrstice = list(igralci[0].keys())
    orodja.zapisi_csv(vrstice, igralci, mapa, datoteka)


def main():
    prenos_strani_tm()
    koncni_seznam_vseh_igralcev = []
    for i in range(1, 21):
        stran_igralcev = igralci_iz_datoteke(tm_directory, f"stran_tm{i}.html")
        koncni_seznam_vseh_igralcev.extend(stran_igralcev)
    zapisi_igralce_v_csv(
        koncni_seznam_vseh_igralcev, tm_directory, "najvrednejsi_igralci.csv"
    )


if __name__ == "__main__":
    main()
