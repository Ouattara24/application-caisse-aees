import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from caisse.models import Membre, Cotisation, Depense, DonFinancier, DonMateriel, ResteAncienneCaisse, AutreArgent, DemandeCarte

# Supprimer tous les enregistrements
Membre.objects.all().delete()
Cotisation.objects.all().delete()
Depense.objects.all().delete()
DonFinancier.objects.all().delete()
DonMateriel.objects.all().delete()
ResteAncienneCaisse.objects.all().delete()
AutreArgent.objects.all().delete()
DemandeCarte.objects.all().delete()

print("✅ Tous les données ont été supprimées")
print("Membres:", Membre.objects.count())
print("Cotisations:", Cotisation.objects.count())
print("Dépenses:", Depense.objects.count())
print("Dons financiers:", DonFinancier.objects.count())
print("Dons matériels:", DonMateriel.objects.count())
print("Restes ancienne caisse:", ResteAncienneCaisse.objects.count())
print("Autres argents:", AutreArgent.objects.count())
print("Demandes carte:", DemandeCarte.objects.count())
