from pathlib import Path

import pandas as pd


# Mapa, v kateri je ta skripta
mapa = Path(__file__).parent

# Poti do datotek
pot_vhodni_csv = mapa / "copilot-chat-activity.csv"
pot_ocisceni_csv = mapa / "copilot-pogovor.csv"
pot_markdown = mapa / "copilot.md"


# Preverimo, ali vhodna datoteka obstaja
if not pot_vhodni_csv.exists():
    raise FileNotFoundError(f"Datoteke ni mogoče najti: {pot_vhodni_csv}")


# Preberemo izvorni CSV
df = pd.read_csv(pot_vhodni_csv)

print("Stolpci v izvorni datoteki:")
print(df.columns.tolist())


# Odstranimo stolpca CreatedAt in ChatName
df = df.drop(columns=["CreatedAt", "ChatName"], errors="ignore")


# Odstranimo vrstice brez vsebine sporočila
df = df.dropna(subset=["MessageContent"])


# Shranimo očiščeni CSV
df.to_csv(pot_ocisceni_csv, index=False, encoding="utf-8-sig")


# Imena avtorjev za prikaz v Markdown datoteki
imena_avtorjev = {
    "user": "Uporabnik",
    "assistant": "Microsoft Copilot",
    "api_tool": "Orodje",
}


# Začetek Markdown dokumenta
deli = [
    "# Pogovor z Microsoft Copilotom",
    "",
    "Ta dokument vsebuje pogovor, uporabljen pri izdelavi projektne naloge.",
    "",
]


# Vsako sporočilo dodamo v Markdown
for _, vrstica in df.iterrows():
    avtor = imena_avtorjev.get(
        vrstica["Author"],
        str(vrstica["Author"]),
    )

    sporocilo = str(vrstica["MessageContent"]).strip()

    # Preskočimo prazna sporočila
    if not sporocilo:
        continue

    deli.append(f"## {avtor}")
    deli.append("")
    deli.append(sporocilo)
    deli.append("")
    deli.append("---")
    deli.append("")


# Shranimo Markdown datoteko
pot_markdown.write_text(
    "\n".join(deli),
    encoding="utf-8",
)


print()
print("Pretvorba je končana.")
print(f"Očiščeni CSV: {pot_ocisceni_csv}")
print(f"Markdown: {pot_markdown}")
print(f"Stolpci v očiščenem CSV-ju: {df.columns.tolist()}")

# Copilot: Naredil funkcijo, ki iz CSV datoteke naredi .md datoteko za pogovor z umetno inteligenco.
