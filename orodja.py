import requests
import os
import csv
from seleniumbase import SB

HEADERS = {"User-agent": "Chrome/148.0.7778.179"}


def prenesi_stran(url):
    try:
        odgovor = requests.get(url, headers=HEADERS, timeout=30)
        odgovor.raise_for_status()
        vsebina = odgovor.text
    except requests.exceptions.RequestException:
        print("spletna stran ni dosegljiva")
        return None
    return vsebina


def prenesi_stran_selenium(url):
    try:
        with SB(uc=True, headless=False) as sb:
            sb.open(url)
            sb.sleep(8)
            vsebina = sb.get_page_source()
    except Exception as e:
        print("spletna stran ni dosegljiva (selenium):", url)
        print("Razlog:", e)
        return None
    return vsebina


def shrani_niz_v_datoteko(besedilo, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8") as file_out:
        file_out.write(besedilo)
    return None


def preberi_datoteko_v_niz(mapa, datoteka):
    pot = os.path.join(mapa, datoteka)
    with open(pot, "r", encoding="utf-8") as file_in:
        besedilo = file_in.read()
    return besedilo


def datoteka_obstaja(mapa, datoteka):
    pot = os.path.join(mapa, datoteka)
    # funkcija os.path.exists sprejme le en argument, zato najprej ustvarimo pot#
    return os.path.exists(pot)


def shrani_naslovno_stran(stran, mapa, datoteka):
    vsebina = prenesi_stran(stran)
    shrani_niz_v_datoteko(vsebina, mapa, datoteka)


def zapisi_csv(stolpci, vrstice, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8", newline="") as csv_file:
        pisatelj = csv.DictWriter(csv_file, fieldnames=stolpci)
        pisatelj.writeheader()
        for vrstica in vrstice:
            pisatelj.writerow(vrstica)
    return
