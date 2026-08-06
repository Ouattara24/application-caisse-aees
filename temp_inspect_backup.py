from pathlib import Path
p = Path("d:/Utilisateur/Documents/APPLICATION-GESTION-CAISSE-AEES/sauvegarde_finale.json")
text = p.read_text(encoding="utf-8", errors="replace")
print("contains:", '"model": "caisse.cotisation"' in text)
print("count:", text.count('"model": "caisse.cotisation"'))
print("count2:", text.count("caisse.cotisation"))
print("sections:", text.count('"model": "caisse.section"'))
