"""
Configuration de l'interface d'administration Django
"""
from django.contrib import admin
from .models import Visiteur, FicheFrais, LigneFraisForfait, LigneFraisHorsForfait, FraisForfait, Etat


@admin.register(Visiteur)
class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'login', 'ville')
    search_fields = ('nom', 'prenom', 'login')
    list_filter = ('ville',)


@admin.register(Etat)
class EtatAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle')


@admin.register(FraisForfait)
class FraisForfaitAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'montant')


@admin.register(FicheFrais)
class FicheFraisAdmin(admin.ModelAdmin):
    list_display = ('idvisiteur', 'mois', 'idetat', 'montantvalide', 'datemodif')
    list_filter = ('idetat', 'mois')
    search_fields = ('idvisiteur__nom', 'idvisiteur__prenom')


@admin.register(LigneFraisForfait)
class LigneFraisForfaitAdmin(admin.ModelAdmin):
    list_display = ('idvisiteur', 'mois', 'idfraisforfait', 'quantite')
    list_filter = ('mois', 'idfraisforfait')


@admin.register(LigneFraisHorsForfait)
class LigneFraisHorsForfaitAdmin(admin.ModelAdmin):
    list_display = ('id', 'idvisiteur', 'mois', 'libelle', 'date', 'montant')
    list_filter = ('mois', 'date')