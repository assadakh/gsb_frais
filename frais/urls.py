"""
URLs de l'application frais
Équivalent du routage dans index.php
"""
from django.urls import path
from . import views

urlpatterns = [
    # Connexion (uc=connexion)
    path('', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    
    # Accueil / Sommaire
    path('accueil/', views.accueil, name='accueil'),
    
    # Gestion des frais (uc=gererFrais)
    path('gerer-frais/', views.gerer_frais, name='gerer_frais'),
    
    # État des frais (uc=etatFrais)
    path('etat-frais/', views.etat_frais, name='etat_frais'),
]