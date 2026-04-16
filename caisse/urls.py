from django.urls import path
from . import views

app_name = 'caisse'

urlpatterns = [
    path('', views.index, name='index'),
    path('membres/', views.MembreListView.as_view(), name='membre_list'),
    path('membres/<int:pk>/modifier/', views.MembreUpdateView.as_view(), name='membre_update'),
    path('membres/<int:pk>/supprimer/', views.MembreDeleteView.as_view(), name='membre_delete'),
    path('bureau-general/', views.BureauGeneralListView.as_view(), name='bureau_general_list'),
    path('membre/ajouter/', views.MembreCreateView.as_view(), name='membre_create'),
    path('membres/section/<int:section_id>/', views.MembreSectionListView.as_view(), name='membre_section_list'),
    path('cotisation/ajouter/', views.CotisationCreateView.as_view(), name='cotisation_create'),
    path('cotisations/', views.cotisations_list, name='cotisations_list'),
    path('cotisations/section/<int:section_id>/', views.cotisations_section_list, name='cotisations_section_list'),
    path('cotisations/bureau-general/', views.cotisations_bureau_general_list, name='cotisations_bureau_general_list'),
    path('cotisations/gestion/', views.CotisationRecordListView.as_view(), name='cotisation_record_list'),
    path('cotisations/payeurs/<str:type_code>/', views.CotisationPayeursByTypeView.as_view(), name='cotisation_payeurs_by_type'),
    path('cotisations/bureau-general/payeurs/<str:type_code>/', views.BureauGeneralCotisationPayeursByTypeView.as_view(), name='bureau_general_cotisation_payeurs_by_type'),
    path('cotisations/section/<int:section_id>/payeurs/<str:type_code>/', views.SectionCotisationPayeursByTypeView.as_view(), name='section_cotisation_payeurs_by_type'),
    path('cotisations/<int:pk>/modifier/', views.CotisationUpdateView.as_view(), name='cotisation_update'),
    path('cotisations/<int:pk>/supprimer/', views.CotisationDeleteView.as_view(), name='cotisation_delete'),
    path('depenses/', views.DepenseListView.as_view(), name='depense_list'),
    path('depense/<int:pk>/modifier/', views.DepenseUpdateView.as_view(), name='depense_update'),
    path('depense/<int:pk>/supprimer/', views.DepenseDeleteView.as_view(), name='depense_delete'),
    path('depense/ajouter/', views.DepenseCreateView.as_view(), name='depense_create'),
    path('don-financier/ajouter/', views.DonFinancierCreateView.as_view(), name='don_financier_create'),
    path('don-materiel/ajouter/', views.DonMaterielCreateView.as_view(), name='don_materiel_create'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
path('create-admin/', views.create_admin),