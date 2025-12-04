"""
Script de test pour valider les fonctionnalites de l'application GSB
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsb_frais.settings')
django.setup()

from frais.models import Visiteur, FicheFrais, LigneFraisForfait, FraisForfait
from frais.utils import est_date_valide, date_francais_vers_anglais, valide_infos_frais

print("=" * 60)
print("TEST DE L'APPLICATION GSB FRAIS")
print("=" * 60)

# Test 1 : Verification des visiteurs
print("\n1. Verification des visiteurs en base...")
visiteurs = Visiteur.objects.all()
print(f"   Nombre de visiteurs : {visiteurs.count()}")
if visiteurs.count() > 0:
    print(f"   Premier visiteur : {visiteurs.first()}")
    print("   [OK]")
else:
    print("   [ERREUR] Aucun visiteur en base")

# Test 2 : Verification des frais forfaitaires
print("\n2. Verification des frais forfaitaires...")
frais_forfait = FraisForfait.objects.all()
print(f"   Nombre de frais forfaitaires : {frais_forfait.count()}")
for frais in frais_forfait:
    print(f"   - {frais.id} : {frais.libelle} ({frais.montant} EUR)")
if frais_forfait.count() == 4:
    print("   [OK]")
else:
    print("   [ERREUR] Il devrait y avoir 4 types de frais forfaitaires")

# Test 3 : Test des fonctions utilitaires
print("\n3. Test des fonctions utilitaires...")

# Test de validation de date
date_test = "20/11/2024"
if est_date_valide(date_test):
    print(f"   - Date valide : {date_test} [OK]")
else:
    print(f"   - Date invalide : {date_test} [ERREUR]")

# Test de conversion de date
date_fr = "20/11/2024"
date_ang = date_francais_vers_anglais(date_fr)
if date_ang == "2024-11-20":
    print(f"   - Conversion date : {date_fr} -> {date_ang} [OK]")
else:
    print(f"   - Conversion date : {date_fr} -> {date_ang} [ERREUR]")

# Test de validation des infos frais
erreurs = valide_infos_frais("20/11/2024", "Test libelle", "50.00")
if len(erreurs) == 0:
    print(f"   - Validation frais valides [OK]")
else:
    print(f"   - Validation frais valides [ERREUR] : {erreurs}")

erreurs = valide_infos_frais("", "", "")
if len(erreurs) > 0:
    print(f"   - Validation frais invalides [OK] : {len(erreurs)} erreurs detectees")
else:
    print(f"   - Validation frais invalides [ERREUR]")

# Test 4 : Test de connexion visiteur
print("\n4. Test de connexion visiteur...")
try:
    visiteur = Visiteur.objects.get(login='dandre', mdp='oppg5')
    print(f"   - Connexion reussie : {visiteur.prenom} {visiteur.nom} [OK]")
except Visiteur.DoesNotExist:
    print("   - Connexion echouee [ERREUR]")

# Test 5 : Verification des fiches de frais
print("\n5. Verification des fiches de frais...")
fiches = FicheFrais.objects.all()
print(f"   Nombre de fiches : {fiches.count()}")
if fiches.count() > 0:
    print("   [OK]")
else:
    print("   [INFO] Aucune fiche de frais creee pour le moment")

print("\n" + "=" * 60)
print("FIN DES TESTS")
print("=" * 60)
