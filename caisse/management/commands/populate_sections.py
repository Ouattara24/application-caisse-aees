from django.core.management.base import BaseCommand
from caisse.models import Section

class Command(BaseCommand):
    help = 'Populate initial sections'

    def handle(self, *args, **options):
        sections = [
            'Sokala-Sobara',
            'Dabakala',
            'Bouaké',
            'Abidjan',
            'Korhogo',
        ]
        for nom in sections:
            Section.objects.get_or_create(nom=nom)
        self.stdout.write(self.style.SUCCESS('Sections créées avec succès'))