from django.http import HttpResponse

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms

from .models import Section, Membre, Cotisation, Depense, DonFinancier, DonMateriel

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'numero_telephone', 'niveau_etude', 'poste_section', 'poste_bureau_general', 'section', 'est_membre_bureau_general']

class CotisationForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['membre', 'montant', 'type']

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['section', 'montant', 'motif']

class DonFinancierForm(forms.ModelForm):
    class Meta:
        model = DonFinancier
        fields = ['montant', 'source']

class DonMaterielForm(forms.ModelForm):
    class Meta:
        model = DonMateriel
        fields = ['description', 'source']

def index(request):
    """Page d'accueil avec boutons pour les différentes actions."""
    sections = Section.objects.all()
    
    # Calculer les cotisations totales par section et par type
    sections_with_totals = []
    for section in sections:
        annuelle_total = Cotisation.objects.filter(
            membre__section=section, 
            type='ANNUELLE'
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        autre_total = Cotisation.objects.filter(
            membre__section=section, 
            type='BOOSTER'
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        sections_with_totals.append({
            'id': section.id,
            'nom': section.nom,
            'annuelle_total': annuelle_total,
            'autre_total': autre_total,
            'total': annuelle_total + autre_total
        })
    
    # Calculer les totaux globaux
    total_annuelle = Cotisation.objects.filter(type='ANNUELLE').aggregate(total=Sum('montant'))['total'] or 0
    total_autre = Cotisation.objects.filter(type='BOOSTER').aggregate(total=Sum('montant'))['total'] or 0
    
    # Calculer les totaux du Bureau Général
    bg_annuelle = Cotisation.objects.filter(
        membre__est_membre_bureau_general=True, 
        type='ANNUELLE'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    bg_autre = Cotisation.objects.filter(
        membre__est_membre_bureau_general=True, 
        type='BOOSTER'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    context = {
        'sections': sections,
        'sections_with_totals': sections_with_totals,
        'total_annuelle': total_annuelle,
        'total_autre': total_autre,
        'bg_annuelle': bg_annuelle,
        'bg_autre': bg_autre,
    }
    
    return render(request, 'caisse/index.html', context)

class MembreListView(ListView):
    model = Membre
    template_name = 'caisse/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('section').order_by('section', 'nom', 'prenom')
        query = self.request.GET.get('q', '')
        section = self.request.GET.get('section', '')
        
        if query:
            queryset = queryset.filter(Q(nom__icontains=query) | Q(prenom__icontains=query))
        
        if section:
            queryset = queryset.filter(section__id=section)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_section'] = self.request.GET.get('section', '')
        return context


class BureauGeneralListView(ListView):
    model = Membre
    template_name = 'caisse/bureau_general_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('section').filter(est_membre_bureau_general=True).order_by('nom', 'prenom')
        query = self.request.GET.get('q', '')
        
        if query:
            queryset = queryset.filter(Q(nom__icontains=query) | Q(prenom__icontains=query))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class MembreCreateView(CreateView):
    model = Membre
    form_class = MembreForm
    template_name = 'caisse/membre_form.html'
    success_url = reverse_lazy('caisse:membre_list')

    def form_valid(self, form):
        messages.success(self.request, 'Membre ajouté avec succès.')
        return super().form_valid(form)


class MembreUpdateView(UpdateView):
    model = Membre
    form_class = MembreForm
    template_name = 'caisse/membre_form.html'
    success_url = reverse_lazy('caisse:membre_list')

    def form_valid(self, form):
        messages.success(self.request, 'Membre modifié avec succès.')
        return super().form_valid(form)


class MembreDeleteView(DeleteView):
    model = Membre
    template_name = 'caisse/membre_confirm_delete.html'
    success_url = reverse_lazy('caisse:membre_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Membre supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

class CotisationCreateView(CreateView):
    model = Cotisation
    form_class = CotisationForm
    template_name = 'caisse/cotisation_form.html'
    success_url = reverse_lazy('caisse:dashboard')

    def get_initial(self):
        initial = super().get_initial()
        cotisation_type = self.request.GET.get('type', '')
        if cotisation_type in dict(Cotisation.TYPE_CHOICES):
            initial['type'] = cotisation_type
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Cotisation ajoutée avec succès.')
        return super().form_valid(form)


class MembreSectionListView(MembreListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        section_id = self.kwargs.get('section_id')
        if section_id:
            queryset = queryset.filter(section__id=section_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_id = self.kwargs.get('section_id')
        if section_id:
            context['selected_section'] = section_id
        return context


class CotisationPayeursByTypeView(ListView):
    model = Membre
    template_name = 'caisse/cotisation_payeurs_by_type.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_type_code(self):
        type_code = self.kwargs.get('type_code', '')
        valid_types = dict(Cotisation.TYPE_CHOICES)
        if type_code not in valid_types:
            raise Http404('Type de cotisation inconnu')
        return type_code

    def get_queryset(self):
        type_code = self.get_type_code()
        return Membre.objects.filter(cotisation__type=type_code).distinct().select_related('section').order_by('section__nom', 'nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_code = self.get_type_code()
        context['type_code'] = type_code
        context['type_label'] = dict(Cotisation.TYPE_CHOICES)[type_code]
        context['payer_count'] = self.get_queryset().count()
        total_sum = Cotisation.objects.filter(type=type_code).aggregate(total=Sum('montant'))['total'] or 0
        context['total_sum'] = total_sum
        return context


class BureauGeneralCotisationPayeursByTypeView(ListView):
    model = Membre
    template_name = 'caisse/cotisation_payeurs_by_type.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_type_code(self):
        type_code = self.kwargs.get('type_code', '')
        valid_types = dict(Cotisation.TYPE_CHOICES)
        if type_code not in valid_types:
            raise Http404('Type de cotisation inconnu')
        return type_code

    def get_queryset(self):
        type_code = self.get_type_code()
        return Membre.objects.filter(cotisation__type=type_code, est_membre_bureau_general=True).distinct().select_related('section').order_by('section__nom', 'nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_code = self.get_type_code()
        context['type_code'] = type_code
        context['type_label'] = dict(Cotisation.TYPE_CHOICES)[type_code]
        context['payer_count'] = self.get_queryset().count()
        context['bureau_general'] = True
        total_sum = Cotisation.objects.filter(membre__est_membre_bureau_general=True, type=type_code).aggregate(total=Sum('montant'))['total'] or 0
        context['total_sum'] = total_sum
        return context


class SectionCotisationPayeursByTypeView(ListView):
    model = Membre
    template_name = 'caisse/cotisation_payeurs_by_type.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_type_code(self):
        type_code = self.kwargs.get('type_code', '')
        valid_types = dict(Cotisation.TYPE_CHOICES)
        if type_code not in valid_types:
            raise Http404('Type de cotisation inconnu')
        return type_code

    def get_section(self):
        section_id = self.kwargs.get('section_id')
        try:
            return Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            raise Http404('Section inconnue')

    def get_queryset(self):
        type_code = self.get_type_code()
        section = self.get_section()
        return Membre.objects.filter(cotisation__type=type_code, section=section).distinct().select_related('section').order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_code = self.get_type_code()
        section = self.get_section()
        context['type_code'] = type_code
        context['type_label'] = dict(Cotisation.TYPE_CHOICES)[type_code]
        context['payer_count'] = self.get_queryset().count()
        context['section'] = section
        total_sum = Cotisation.objects.filter(membre__section=section, type=type_code).aggregate(total=Sum('montant'))['total'] or 0
        context['total_sum'] = total_sum
        return context


class DepenseCreateView(CreateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'caisse/depense_form.html'
    success_url = reverse_lazy('caisse:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_depenses_global'] = Depense.objects.aggregate(total=Sum('montant'))['total'] or 0
        context['total_cotisations'] = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
        context['total_dons'] = DonFinancier.objects.aggregate(total=Sum('montant'))['total'] or 0
        context['solde_general'] = context['total_cotisations'] + context['total_dons'] - context['total_depenses_global']
        context['depenses_par_section'] = Depense.objects.values('section__nom').annotate(total=Sum('montant')).order_by('section__nom')
        context['cotisations_par_section'] = Cotisation.objects.values('membre__section__nom').annotate(total=Sum('montant')).order_by('membre__section__nom')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Dépense ajoutée avec succès.')
        return super().form_valid(form)


class DonFinancierCreateView(CreateView):
    model = DonFinancier
    form_class = DonFinancierForm
    template_name = 'caisse/don_financier_form.html'
    success_url = reverse_lazy('caisse:dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Don financier ajouté avec succès.')
        return super().form_valid(form)


class DonMaterielCreateView(CreateView):
    model = DonMateriel
    form_class = DonMaterielForm
    template_name = 'caisse/don_materiel_form.html'
    success_url = reverse_lazy('caisse:dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Don matériel ajouté avec succès.')
        return super().form_valid(form)


class CotisationRecordListView(ListView):
    model = Cotisation
    template_name = 'caisse/cotisation_record_list.html'
    context_object_name = 'cotisations'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('membre', 'membre__section').order_by('-date')
        section = self.request.GET.get('section', '')
        query = self.request.GET.get('q', '')

        if section:
            queryset = queryset.filter(membre__section__id=section)
        if query:
            queryset = queryset.filter(Q(membre__nom__icontains=query) | Q(membre__prenom__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_section'] = self.request.GET.get('section', '')
        context['total_par_section'] = Cotisation.objects.values('membre__section__nom').annotate(total=Sum('montant')).order_by('membre__section__nom')
        context['total_global'] = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
        return context


class CotisationUpdateView(UpdateView):
    model = Cotisation
    form_class = CotisationForm
    template_name = 'caisse/cotisation_form.html'
    success_url = reverse_lazy('caisse:cotisation_record_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cotisation modifiée avec succès.')
        return super().form_valid(form)


class CotisationDeleteView(DeleteView):
    model = Cotisation
    template_name = 'caisse/cotisation_confirm_delete.html'
    success_url = reverse_lazy('caisse:cotisation_record_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cotisation supprimée avec succès.')
        return super().delete(request, *args, **kwargs)


class DepenseListView(ListView):
    model = Depense
    template_name = 'caisse/depense_list.html'
    context_object_name = 'depenses'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('section').order_by('-date')
        section = self.request.GET.get('section', '')
        query = self.request.GET.get('q', '')

        if section:
            queryset = queryset.filter(section__id=section)
        if query:
            queryset = queryset.filter(motif__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_section'] = self.request.GET.get('section', '')

        context['total_depenses_global'] = Depense.objects.aggregate(total=Sum('montant'))['total'] or 0
        context['total_cotisations'] = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
        context['total_dons'] = DonFinancier.objects.aggregate(total=Sum('montant'))['total'] or 0
        context['solde_general'] = (context['total_cotisations'] + context['total_dons'] - context['total_depenses_global'])
        context['depenses_par_section'] = Depense.objects.values('section__nom').annotate(total=Sum('montant')).order_by('section__nom')
        context['cotisations_par_section'] = Cotisation.objects.values('membre__section__nom').annotate(total=Sum('montant')).order_by('membre__section__nom')

        # section-specific balances (optionnel)
        section_id = self.request.GET.get('section')
        if section_id:
            section_obj = Section.objects.filter(id=section_id).first()
            if section_obj:
                section_total = Cotisation.objects.filter(membre__section=section_obj).aggregate(total=Sum('montant'))['total'] or 0
                section_depense = Depense.objects.filter(section=section_obj).aggregate(total=Sum('montant'))['total'] or 0
                context['section_name'] = section_obj.nom
                context['section_total_cotise'] = section_total
                context['section_total_depense'] = section_depense
                context['section_solde'] = section_total - section_depense

        return context


class DepenseUpdateView(UpdateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'caisse/depense_form.html'
    success_url = reverse_lazy('caisse:depense_list')

    def form_valid(self, form):
        messages.success(self.request, 'Dépense modifiée avec succès.')
        return super().form_valid(form)


class DepenseDeleteView(DeleteView):
    model = Depense
    template_name = 'caisse/depense_confirm_delete.html'
    success_url = reverse_lazy('caisse:depense_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Dépense supprimée avec succès.')
        return super().delete(request, *args, **kwargs)


def cotisations_list(request):
    """Liste de tous les membres ayant cotisé avec le total par membre."""
    from django.core.paginator import Paginator
    from django.db.models import Sum
    
    page_number = request.GET.get('page')
    
    # Utiliser une requête optimisée avec select_related et annotate
    cotisations_groupe = Cotisation.objects.select_related('membre__section').values(
        'membre', 'membre__nom', 'membre__prenom', 'membre__section__nom'
    ).annotate(total=Sum('montant')).order_by('membre__nom', 'membre__prenom')
    
    paginator = Paginator(cotisations_groupe, 10)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
    }
    return render(request, 'caisse/cotisations_list.html', context)

def cotisations_section_list(request, section_id):
    """Liste des membres ayant cotisé dans une section."""
    from django.core.paginator import Paginator
    from django.db.models import Sum
    
    section = get_object_or_404(Section, pk=section_id)
    page_number = request.GET.get('page')
    
    cotisations_groupe = Cotisation.objects.select_related('membre__section').filter(membre__section=section).values(
        'membre', 'membre__nom', 'membre__prenom', 'membre__section__nom'
    ).annotate(total=Sum('montant')).order_by('membre__nom', 'membre__prenom')
    
    paginator = Paginator(cotisations_groupe, 10)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'section': section,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
    }
    return render(request, 'caisse/cotisations_section_list.html', context)

def cotisations_bureau_general_list(request):
    """Liste des membres du bureau général ayant cotisé."""
    from django.core.paginator import Paginator
    from django.db.models import Sum
    
    page_number = request.GET.get('page')
    
    cotisations_groupe = Cotisation.objects.select_related('membre__section').filter(membre__est_membre_bureau_general=True).values(
        'membre', 'membre__nom', 'membre__prenom', 'membre__section__nom'
    ).annotate(total=Sum('montant')).order_by('membre__nom', 'membre__prenom')
    
    paginator = Paginator(cotisations_groupe, 10)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
    }
    sections = Section.objects.all()
    sections = Section.objects.all()

context = {
    'sections': sections,
    'cotisations_par_section': cotisations_par_section,
    'depenses_par_section': depenses_par_section,
    'solde_general': solde_general,
    'payeurs_bureau': payeurs_bureau,
    'total_depenses': total_depenses,
    'toutes_cotisations': toutes_cotisations,
    'toutes_depenses': toutes_depenses,
}

return render(request, 'caisse/dashboard.html', context)

def dashboard(request):
    """Tableau de bord avec statistiques."""
    # Cotisations par section
    cotisations_par_section = {}
    depenses_par_section = {}
    for section in Section.objects.all():
        cotisations = Cotisation.objects.filter(membre__section=section).aggregate(sum=Sum('montant'))['sum'] or 0
        depenses = Depense.objects.filter(section=section).aggregate(sum=Sum('montant'))['sum'] or 0
        cotisations_par_section[section.nom] = cotisations
        depenses_par_section[section.nom] = depenses

    # Solde général
    total_cotisations = Cotisation.objects.aggregate(sum=Sum('montant'))['sum'] or 0
    total_depenses = Depense.objects.aggregate(sum=Sum('montant'))['sum'] or 0
    total_dons_financiers = DonFinancier.objects.aggregate(sum=Sum('montant'))['sum'] or 0
    solde_general = total_cotisations + total_dons_financiers - total_depenses

    # Membres bureau général ayant payé
    membres_bureau = Membre.objects.filter(est_membre_bureau_general=True)
    payeurs_bureau = Cotisation.objects.filter(membre__in=membres_bureau).values('membre').distinct().count()

    # Toutes les cotisations
    toutes_cotisations = Cotisation.objects.all()

    # Toutes les dépenses
    toutes_depenses = Depense.objects.all()

    return render(request, 'caisse/dashboard.html', {
        'cotisations_par_section': cotisations_par_section,
        'depenses_par_section': depenses_par_section,
        'total_depenses': total_depenses,
        'solde_general': solde_general,
        'payeurs_bureau': payeurs_bureau,
        'toutes_cotisations': toutes_cotisations,
        'toutes_depenses': toutes_depenses,
    })

   from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "", "2410ouatt")
        return HttpResponse("Admin créé avec succès")
    return HttpResponse("Admin existe déjà")