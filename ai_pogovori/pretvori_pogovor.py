import pandas as pd

df = pd.read_csv("ai_pogovori/copilot-chat-activity.csv")

# Odstranimo prazna sporočila
df = df.dropna(subset=["MessageContent"])

imena_avtorjev = {
    "user": "Uporabnik",
    "assistant": "Microsoft Copilot",
    "api_tool": "Orodje",
}

deli = [
    "# Pogovor z Microsoft Copilotom",
    "",
    "Ta dokument vsebuje pogovor, uporabljen pri izdelavi projektne naloge.",
    "",
]

for _, vrstica in df.iterrows():
    avtor = imena_avtorjev.get(vrstica["Author"], str(vrstica["Author"]))

    sporocilo = str(vrstica["MessageContent"]).strip()

    deli.append(f"## {avtor}")
    deli.append("")
    deli.append(sporocilo)
    deli.append("")
    deli.append("---")
    deli.append("")

with open("copilot.md", "w", encoding="utf-8") as datoteka:
    datoteka.write("\n".join(deli))

print("Datoteka copilot.md je bila uspešno ustvarjena.")
# Copilot: Naredil datoteko, ki spremeni CSV datoteko v .md datoteko za oddajo pogovora.
