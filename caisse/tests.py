from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Cotisation, Depense, DonFinancier, DonMateriel, AutreArgent, ResteAncienneCaisse, Section, Membre

User = get_user_model()


class CaisseAppFeaturesTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(nom='Sokala-Sobara')
        self.section_b = Section.objects.create(nom='Abidjan')
        self.membre = Membre.objects.create(
            nom='Kouassi',
            prenom='Jean',
            section=self.section,
        )
        self.cotisation = Cotisation.objects.create(
            membre=self.membre,
            montant=25000,
            type='BOOSTER',
        )
        self.don_financier = DonFinancier.objects.create(montant=5000, source='Sponsor')
        self.don_materiel = DonMateriel.objects.create(description='Ordinateur', source='Donateur')
        self.autre_argent = AutreArgent.objects.create(montant=3000, source='Vente')
        self.reste_ancienne_caisse = ResteAncienneCaisse.objects.create(montant=2000, description='Solde')
        self.depense = Depense.objects.create(section=self.section, montant=1500, motif='Achat matériel')

    def test_cotisation_exceptionnelle_is_used_in_choices(self):
        self.assertIn(('BOOSTER', 'Cotisation exceptionnelle'), Cotisation.TYPE_CHOICES)

    def test_dashboard_has_edit_and_delete_actions_for_records(self):
        response = self.client.get(reverse('caisse:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cotisation exceptionnelle')
        self.assertContains(response, 'Dons financiers récents')
        self.assertContains(response, 'Dons matériels récents')
        self.assertContains(response, reverse('caisse:don_financier_update', args=[self.don_financier.pk]))
        self.assertContains(response, reverse('caisse:don_financier_delete', args=[self.don_financier.pk]))
        self.assertContains(response, reverse('caisse:don_materiel_update', args=[self.don_materiel.pk]))
        self.assertContains(response, reverse('caisse:don_materiel_delete', args=[self.don_materiel.pk]))
        self.assertContains(response, reverse('caisse:autre_argent_update', args=[self.autre_argent.pk]))
        self.assertContains(response, reverse('caisse:autre_argent_delete', args=[self.autre_argent.pk]))
        self.assertContains(response, reverse('caisse:reste_ancienne_caisse_update', args=[self.reste_ancienne_caisse.pk]))
        self.assertContains(response, reverse('caisse:reste_ancienne_caisse_delete', args=[self.reste_ancienne_caisse.pk]))

    def test_depense_filter_and_reset_are_functional(self):
        response = self.client.get(reverse('caisse:depense_list'), {'q': 'Achat', 'section': self.section.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Achat matériel')
        self.assertContains(response, reverse('caisse:depense_list'))

        response_reset = self.client.get(reverse('caisse:depense_list'))
        self.assertEqual(response_reset.status_code, 200)
        self.assertContains(response_reset, 'Réinitialiser')

    def test_cotisation_record_filter_and_reset_are_functional(self):
        response = self.client.get(reverse('caisse:cotisation_record_list'), {'q': 'Jean', 'section': self.section.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jean')
        self.assertContains(response, reverse('caisse:cotisation_record_list'))

        response_reset = self.client.get(reverse('caisse:cotisation_record_list'))
        self.assertEqual(response_reset.status_code, 200)
        self.assertContains(response_reset, 'Réinitialiser')

    def test_admin_access_page_allows_permission_assignment(self):
        admin = User.objects.create_superuser(username='admin_test', password='admin123', email='')
        user = User.objects.create_user(username='gestionnaire', password='gestion123')
        self.client.force_login(admin)

        permission = Permission.objects.filter(codename='view_membre').first()
        response = self.client.post(
            reverse('caisse:admin_access_control'),
            {
                f'user_{user.pk}_staff': 'on',
                f'user_{user.pk}_active': 'on',
                f'user_{user.pk}_perm_{permission.pk}': 'on',
            },
        )

        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.has_perm('caisse.view_membre'))

    def test_admin_home_dashboard_shows_active_user_summary(self):
        admin = User.objects.create_superuser(username='admin_summary', password='admin123', email='')
        User.objects.create_user(username='active_user', password='test123', is_active=True)
        User.objects.create_user(username='inactive_user', password='test123', is_active=False)
        self.client.force_login(admin)

        response = self.client.get(reverse('caisse:index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_users_count'], 2)
        self.assertContains(response, 'Utilisateurs actifs')

    def test_admin_home_dashboard_shows_recent_connected_users(self):
        admin = User.objects.create_superuser(username='admin_recent', password='admin123', email='')
        recent_user = User.objects.create_user(username='recent_user', password='test123', is_active=True)
        older_user = User.objects.create_user(username='older_user', password='test123', is_active=True)
        recent_user.last_login = '2024-01-15 10:00:00'
        older_user.last_login = '2024-01-10 10:00:00'
        recent_user.save(update_fields=['last_login'])
        older_user.save(update_fields=['last_login'])
        self.client.force_login(admin)

        response = self.client.get(reverse('caisse:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_user', [u['username'] for u in response.context['recent_users']])
        self.assertContains(response, 'Derniers utilisateurs connectés')

    def test_user_registration_requires_six_character_password(self):
        response = self.client.post(
            reverse('caisse:register'),
            {
                'username': 'nouvelutilisateur',
                'password1': '123456',
                'password2': '123456',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='nouvelutilisateur').exists())

    def test_admin_access_page_shows_checked_permissions_for_assigned_users(self):
        admin = User.objects.create_superuser(username='admin_perm_check', password='admin123', email='')
        user = User.objects.create_user(username='permission_user', password='gestion123')
        permission = Permission.objects.filter(codename='view_membre').first()
        user.user_permissions.add(permission)
        self.client.force_login(admin)

        response = self.client.get(reverse('caisse:admin_access_control'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'name="user_{user.pk}_perm_{permission.pk}"')
        self.assertContains(response, 'checked')
