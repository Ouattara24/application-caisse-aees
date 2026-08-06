from pathlib import Path
p = Path('d:/Utilisateur/Documents/APPLICATION-GESTION-CAISSE-AEES/sauvegarde_finale.json')
text = p.read_text(encoding='utf-16')
print('cotisation count:', text.count('cotisation'))
print('cotisation begin:', text.find('cotisation'))
print(text[text.find('cotisation')-50:text.find('cotisation')+150])
