from django.contrib import admin
from .models import Section, Membre, Cotisation, Depense, DonFinancier, DonMateriel

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'numero_telephone', 'section', 'est_membre_bureau_general')
    list_filter = ('section', 'est_membre_bureau_general', 'niveau_etude')
    search_fields = ('nom', 'prenom', 'numero_telephone')

@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    list_display = ('membre', 'montant', 'type', 'date')
    list_filter = ('type', 'date')

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('section', 'montant', 'motif', 'date')
    list_filter = ('section', 'date')

@admin.register(DonFinancier)
class DonFinancierAdmin(admin.ModelAdmin):
    list_display = ('montant', 'source', 'date')

@admin.register(DonMateriel)
class DonMaterielAdmin(admin.ModelAdmin):
    list_display = ('description', 'source', 'date')

