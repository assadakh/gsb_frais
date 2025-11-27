"""
URL configuration for gsb_frais project.
Équivalent du routage principal dans index.php
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Interface d'administration Django
    path('', include('frais.urls')),  # Toutes les URLs de l'application frais
]