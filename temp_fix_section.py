import os
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
import django
django.setup()
from caisse.models import Section
bad = ['BouakÚ', 'Bouak┌']
print('before:', [repr(s.nom) for s in Section.objects.filter(nom__in=bad)])
for b in bad:
    q = Section.objects.filter(nom=b)
    if q.exists():
        q.update(nom='Bouaké')
print('after:', [repr(s.nom) for s in Section.objects.filter(nom='Bouaké')])
