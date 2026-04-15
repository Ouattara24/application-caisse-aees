from django.db import models

class Section(models.Model):
    """Une section de l'AEES."""
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'section'
        verbose_name_plural = 'sections'


class Membre(models.Model):
    """Un membre de l'AEES."""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=20, blank=True)
    niveau_etude = models.CharField(max_length=100, blank=True)
    poste_section = models.CharField(max_length=100, blank=True)
    poste_bureau_general = models.CharField(max_length=100, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    est_membre_bureau_general = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.section.nom})"

    class Meta:
        verbose_name = 'membre'
        verbose_name_plural = 'membres'
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['section']),
            models.Index(fields=['est_membre_bureau_general']),
        ]


class Cotisation(models.Model):
    """Une cotisation payée par un membre."""
    TYPE_CHOICES = [
        ('ANNUELLE', 'Annuelle'),
        ('BOOSTER', 'Autre cotisation'),
    ]

    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cotisation {self.type} de {self.membre} - {self.montant}"

    class Meta:
        verbose_name = 'cotisation'
        verbose_name_plural = 'cotisations'
        indexes = [
            models.Index(fields=['membre']),
            models.Index(fields=['type']),
            models.Index(fields=['date']),
        ]


class Depense(models.Model):
    """Une dépense effectuée par une section."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    motif = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dépense {self.section.nom} - {self.montant} ({self.motif})"

    class Meta:
        verbose_name = 'dépense'
        verbose_name_plural = 'dépenses'
        indexes = [
            models.Index(fields=['section']),
            models.Index(fields=['date']),
        ]


class DonFinancier(models.Model):
    """Un don financier reçu par l'AEES."""
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don financier de {self.source} - {self.montant}"

    class Meta:
        verbose_name = 'don financier'
        verbose_name_plural = 'dons financiers'


class DonMateriel(models.Model):
    """Un don matériel reçu par l'AEES."""
    description = models.TextField()
    source = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don matériel de {self.source} - {self.description}"

    class Meta:
        verbose_name = 'don matériel'
        verbose_name_plural = 'dons matériels'

