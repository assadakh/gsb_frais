"""
Configuration de l'application frais
"""
from django.apps import AppConfig


class FraisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frais'
    verbose_name = 'Gestion des Frais GSB'