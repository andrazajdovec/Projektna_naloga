import time
import random
import orodja
import re

# URL glavne strani Transfermarkta
tm_URL = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page="
# mapa v kateri bodo shranjeni podatki
tm_mapa = "podatki/transfermarkt"


# Prenese 20 strani lestvice najvrednejših igralcev in jih shrani v HTML-datoteke
def prenos_strani_tm():
    for i in range(1, 21):
        if orodja.datoteka_obstaja(tm_mapa, f"stran_tm{i}.html") is True:
            continue

        odgovor = orodja.prenesi_stran(f"{tm_URL}{i}")
        if odgovor is None:
            print("napaka", i)
            continue

        orodja.shrani_niz_v_datoteko(odgovor, tm_mapa, f"stran_tm{i}.html")

        time.sleep(random.uniform(2, 3))
        # Copilot: predlagan časovni interval za time.sleep()


# Razdeli HTML tabele na posamezne bloke, kjer vsak blok predstavlja enega igraalca
def stran_v_blok(besedilo):
    return re.findall(
        r'<tr class="(?:odd|even)">.*?(?=<tr class="(?:odd|even)">|$)',
        besedilo,
        flags=re.DOTALL,
    )
    # Copilot: Popravil regularni izraz, da je pravilno zajel vsakega igralca v svoj blok.


# Pomožna funkcija, ki vse vrednosti pretvori v milijone in v float
def pretvori_vrednost(vrednost):
    if "m" in vrednost:
        return float(vrednost[:-1])
    elif "k" in vrednost:
        return float(vrednost[:-1]) / 1000


# Iz HTML-bloka posameznega igralca izlušči osnovne podatke in jih vrne kot slovar
def izlusci_podatke_igralca(blok):
    uvrstitev = re.search(r'<td class="zentriert">(\d+)</td>', blok)
    ime = re.search(r'<td class="hauptlink"><a .*?>(.*?)</a>', blok)
    starost = re.search(r'</td><td class="zentriert">(\d+)</td>', blok)
    drzavljanstvo = re.search(
        r'<td class="zentriert"><img src=.*?title="(.*?)" alt=', blok
    )
    klub = re.search(r'<td class="zentriert"><a title="(.*?)" href="/', blok)
    vrednost = re.search(r'<a href="/.*?>€(.*?)</a>', blok)

    # Če kateri od podatkov manjka, igralca izpustimo
    if (
        uvrstitev is None
        or ime is None
        or starost == None
        or drzavljanstvo is None
        or klub is None
        or vrednost is None
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


# Iz ene HTML-datoteke pripravi seznam veljavnih igralcev
def igralci_iz_datoteke(mapa, datoteka):
    vsebina = orodja.preberi_datoteko_v_niz(mapa, datoteka)
    bloki = stran_v_blok(vsebina)
    igralci = [izlusci_podatke_igralca(blok) for blok in bloki]
    return [igralec for igralec in igralci if igralec is not None]


def zapisi_igralce_v_csv(igralci, mapa, datoteka):
    assert igralci and (all(igralec.keys() == igralci[0].keys() for igralec in igralci))
    vrstice = list(igralci[0].keys())
    orodja.zapisi_csv(vrstice, igralci, mapa, datoteka)


# Izvede celoten postopek: prenese strani, izlušči igralce in jih zapiše v CSV
def main():
    prenos_strani_tm()

    koncni_seznam_vseh_igralcev = []

    for i in range(1, 21):
        stran_igralcev = igralci_iz_datoteke(tm_mapa, f"stran_tm{i}.html")
        koncni_seznam_vseh_igralcev.extend(stran_igralcev)

    zapisi_igralce_v_csv(
        koncni_seznam_vseh_igralcev, tm_mapa, "najvrednejsi_igralci.csv"
    )


if __name__ == "__main__":
    main()
